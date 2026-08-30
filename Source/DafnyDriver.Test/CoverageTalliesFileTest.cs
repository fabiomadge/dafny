using System;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Dafny;
using Microsoft.Dafny.Compilers;
using Xunit;

namespace DafnyDriver.Test;

public class CoverageTalliesFileTest {

  [Fact]
  public Task ExecutionCoverageLeavesNoTalliesFile() =>
    AssertNoTalliesFileRemains("--target:cs", output => Assert.Contains("a", output));

  // The instrumenter is constructed before the unsupported-target check rejects the run.
  [Fact]
  public Task UnsupportedTargetLeavesNoTalliesFile() =>
    AssertNoTalliesFileRemains("--target:py", output => Assert.Contains("not supported", output));

  // Matched by CoverageInstrumenter.TalliesFilePrefix rather than by a name spelled out here, so
  // that the assertion cannot go quiet if the file is ever named differently. The directory is not
  // required to be empty: System.CommandLine, MSBuild and Roslyn leave state of their own in it.
  private static async Task AssertNoTalliesFileRemains(string target, Action<string> checkOutput) {
    var sandbox = Path.Combine(Path.GetTempPath(), Path.GetRandomFileName());
    var temp = Path.Combine(sandbox, "temp");
    Directory.CreateDirectory(temp);
    var source = Path.Combine(sandbox, "cov.dfy");
    await File.WriteAllTextAsync(source,
      "method Main() { var i := 0; if i == 0 { print \"a\\n\"; } else { print \"b\\n\"; } }\n");

    var restoreTemp = RedirectTempTo(temp);
    try {
      var output = new StringWriter();
      // --no-verify so this does not depend on a solver being present.
      await DafnyBackwardsCompatibleCli.MainWithWriters(output, output, TextReader.Null,
        ["run", target, "--no-verify", "--coverage-report", Path.Combine(sandbox, "report"), source]);
      checkOutput(output.ToString());

      var leaked = Directory.GetFiles(temp, CoverageInstrumenter.TalliesFilePrefix + "*");
      Assert.True(leaked.Length == 0,
        "tallies file left behind: " + string.Join(", ", leaked.Select(Path.GetFileName)));
    } finally {
      restoreTemp();
      try {
        Directory.Delete(sandbox, true);
      } catch (IOException) {
      }
    }
  }

  // Which variable GetTempPath consults differs by platform, so all three are set. It is
  // process-wide, which is why this assembly disables test parallelization.
  private static Action RedirectTempTo(string directory) {
    string[] variables = ["TMPDIR", "TMP", "TEMP"];
    var previous = variables.Select(Environment.GetEnvironmentVariable).ToArray();
    foreach (var variable in variables) {
      Environment.SetEnvironmentVariable(variable, directory + Path.DirectorySeparatorChar);
    }
    Assert.Equal(directory + Path.DirectorySeparatorChar, Path.GetTempPath());
    return () => {
      for (var i = 0; i < variables.Length; i++) {
        Environment.SetEnvironmentVariable(variables[i], previous[i]);
      }
    };
  }
}
