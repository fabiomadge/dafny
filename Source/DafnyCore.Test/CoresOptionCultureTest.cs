using System;
using System.CommandLine;
using System.Globalization;
using System.Threading;
using Microsoft.Dafny;
using Xunit;

namespace DafnyCore.Test;

public class CoresOptionCultureTest {

  // On a thread of its own, because xunit reuses pool threads across concurrent tests.
  private static (uint Cores, string? Error) ParseCores(string value, string culture) {
    uint cores = 0;
    string? error = null;
    Exception? failure = null;
    var thread = new Thread(() => {
      CultureInfo.CurrentCulture = new CultureInfo(culture);
      try {
        var command = new Command("test") { BoogieOptionBag.Cores };
        var parsed = command.Parse(["test", $"--cores={value}"]);
        error = parsed.Errors.Count == 0 ? null : parsed.Errors[0].Message;
        if (error == null) {
          cores = parsed.GetValueForOption(BoogieOptionBag.Cores);
        }
      } catch (Exception e) {
        failure = e;
      }
    });
    thread.Start();
    Assert.True(thread.Join(60_000), "parsing did not finish");
    Assert.Null(failure);
    return (cores, error);
  }

  // "." groups digits in de-DE, so "50.5%" used to parse as 505%.
  [Theory]
  [InlineData("50.5%")]
  [InlineData("12.5%")]
  [InlineData("1e2%")]
  public void PercentageMeansTheSameInEveryCulture(string value) {
    var fractionSeparator = ParseCores(value, "en-US");
    var digitGrouping = ParseCores(value, "de-DE");

    Assert.Null(fractionSeparator.Error);
    Assert.Equal(fractionSeparator, digitGrouping);
  }

  [Theory]
  [InlineData("en-US")]
  [InlineData("de-DE")]
  public void WholePercentageOfEveryCoreIsEveryCore(string culture) {
    Assert.Equal((uint)Environment.ProcessorCount, ParseCores("100%", culture).Cores);
  }

  [Theory]
  [InlineData("en-US")]
  [InlineData("de-DE")]
  public void ThousandsSeparatorIsRejectedRatherThanGuessed(string culture) {
    // "1,000" means 1 under a comma-decimal culture and 1000 under a comma-grouping one.
    Assert.Contains("Could not parse percentage", ParseCores("1,000%", culture).Error);
  }

  // Float accepts NaN and Infinity, and the cast to uint is unchecked.
  [Theory]
  [InlineData("NaN%")]
  [InlineData("Infinity%")]
  [InlineData("-Infinity%")]
  [InlineData("1e30%")]
  public void UnrepresentablePercentageIsRejected(string value) {
    Assert.Contains("does not denote a usable number of cores", ParseCores(value, "en-US").Error);
  }

  // These silently meant one core, while `--cores:0` has always been an error.
  [Theory]
  [InlineData("0%")]
  [InlineData("-50%")]
  [InlineData("-0.5%")]
  public void NonPositivePercentageIsRejectedLikeAnExplicitZero(string value) {
    var error = ParseCores(value, "en-US").Error;

    Assert.Contains("must be greater than 0", error);
    Assert.Equal(ParseCores("0", "en-US").Error, error);
  }

  [Fact]
  public void PercentageRoundingDownToZeroStillMeansOneCore() {
    Assert.Equal(1U, ParseCores("0.0001%", "en-US").Cores);
  }
}
