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

  /// <summary>
  /// A target that does not support execution coverage rejects it, but the instrumenter is
  /// constructed before that check, so creating the tallies file eagerly left one behind on every
  /// such invocation with no report to show for it.
  /// </summary>
  [Fact]
  public Task UnsupportedTargetLeavesNoTalliesFile() =>
    AssertNoTalliesFileRemains("--target:py", output => Assert.Contains("not supported", output));

  /// <summary>
  /// Runs `dafny run --coverage-report` for "target" with the temp directory pointed at one of its
  /// own, and requires that no tallies file survives.
  ///
  /// Matched by <see cref="CoverageInstrumenter.TalliesFilePrefix"/> rather than by a name spelled
  /// out here, so that the assertion cannot go quiet if the file is ever named differently. The
  /// directory is not required to be empty: System.CommandLine, MSBuild and Roslyn all leave state
  /// of their own behind in it, and none of that is Dafny's to clean up.
  /// </summary>
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
      // --no-verify: this is about cleaning up a temp file, so there is no reason to depend on a
      // solver being present.
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

  /// <summary>
  /// Points Path.GetTempPath() at "directory" and returns an action restoring the previous value.
  /// The variable consulted differs by platform -- TMPDIR on Unix, TMP/TEMP on Windows -- so all
  /// three are set. GetTempPath reads them on each call rather than caching, so this takes effect
  /// immediately. It is process-wide, which is why this assembly disables test parallelization.
  /// </summary>
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
