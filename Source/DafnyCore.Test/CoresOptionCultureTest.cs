using System;
using System.CommandLine;
using System.Globalization;
using System.Threading;
using Microsoft.Dafny;
using Xunit;

namespace DafnyCore.Test;

public class CoresOptionCultureTest {

  /// <summary>
  /// Parses "--cores=&lt;value&gt;" with "culture" as the ambient culture, returning the resulting
  /// core count and any parse error. The culture is set on a thread this test owns, because xunit
  /// runs test classes in parallel on pool threads it reuses.
  /// </summary>
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

  /// <summary>
  /// A command-line value is not written in the ambient locale's number format. "de-DE" groups
  /// digits with "." rather than separating the fraction with it, so on master "50.5%" parsed as
  /// 505%, asking for five times the machine's cores.
  /// </summary>
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
    // Pins what a percentage means, without restating the rounding for a fractional one.
    Assert.Equal((uint)Environment.ProcessorCount, ParseCores("100%", culture).Cores);
  }

  [Theory]
  [InlineData("en-US")]
  [InlineData("de-DE")]
  public void ThousandsSeparatorIsRejectedRatherThanGuessed(string culture) {
    // "1,000" means 1 under a comma-decimal culture and 1000 under a comma-grouping one.
    Assert.Contains("Could not parse percentage", ParseCores("1,000%", culture).Error);
  }

  /// <summary>
  /// NumberStyles.Float accepts "NaN" and "Infinity", and casting either to uint is unchecked, so
  /// they would silently become 1 core and uint.MaxValue cores. A finite product that does not fit
  /// in a uint is rejected for the same reason: the cast would wrap rather than report.
  /// </summary>
  [Theory]
  [InlineData("NaN%")]
  [InlineData("Infinity%")]
  [InlineData("-Infinity%")]
  [InlineData("1e30%")]
  public void UnrepresentablePercentageIsRejected(string value) {
    Assert.Contains("does not denote a usable number of cores", ParseCores(value, "en-US").Error);
  }

  /// <summary>
  /// `--cores:0` has always been an error, but `--cores:0%` silently meant one core, as did any
  /// negative percentage.
  /// </summary>
  [Theory]
  [InlineData("0%")]
  [InlineData("-50%")]
  [InlineData("-0.5%")]
  public void NonPositivePercentageIsRejectedLikeAnExplicitZero(string value) {
    Assert.Equal(ParseCores("0", "en-US").Error, ParseCores(value, "en-US").Error);
    Assert.Contains("must be greater than 0", ParseCores(value, "en-US").Error);
  }

  [Fact]
  public void PercentageRoundingDownToZeroStillMeansOneCore() {
    Assert.Equal(1U, ParseCores("0.0001%", "en-US").Cores);
  }
}
