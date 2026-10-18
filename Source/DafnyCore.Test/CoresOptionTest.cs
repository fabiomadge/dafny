using System.CommandLine;
using System.Globalization;
using Microsoft.Dafny;

namespace DafnyCore.Test;

public class CoresOptionTest {
  private static (uint Cores, string? Error) ParseCores(string value, string culture) {
    var ambient = CultureInfo.CurrentCulture;
    CultureInfo.CurrentCulture = new CultureInfo(culture);
    try {
      var result = BoogieOptionBag.Cores.Parse(["--cores", value]);
      return result.Errors.Count == 0
        ? (result.GetValueForOption(BoogieOptionBag.Cores), null)
        : (0, result.Errors[0].Message);
    }
    finally {
      CultureInfo.CurrentCulture = ambient;
    }
  }

  // 100.0% is every core on any machine. Under de-DE "." groups digits, so a parse in the ambient culture
  // reads 1000%; under fr-FR it fails.
  [Theory]
  [InlineData("de-DE")]
  [InlineData("fr-FR")]
  public void PercentageIgnoresTheAmbientCulture(string culture) {
    var (cores, error) = ParseCores("100.0%", culture);
    Assert.Null(error);
    Assert.Equal((uint)Environment.ProcessorCount, cores);
  }

  [Theory]
  [InlineData("50,5%")]
  [InlineData("NaN%")]
  [InlineData("Infinity%")]
  [InlineData("-50%")]
  [InlineData("2147483648")]
  public void InvalidValueIsRejected(string value) {
    Assert.NotNull(ParseCores(value, CultureInfo.InvariantCulture.Name).Error);
  }

  // More cores than int.MaxValue, but fewer than uint.MaxValue, on any machine.
  [Fact]
  public void PercentageBeyondIntMaxValueCoresIsRejected() {
    var percentage = (1.5 * int.MaxValue / Environment.ProcessorCount * 100).ToString(CultureInfo.InvariantCulture);
    Assert.NotNull(ParseCores($"{percentage}%", CultureInfo.InvariantCulture.Name).Error);
  }
}
