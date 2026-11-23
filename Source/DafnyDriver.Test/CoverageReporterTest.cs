using Microsoft.Dafny;

namespace DafnyDriver.Test;

public class CoverageReporterTest {

  [Fact]
  public async Task ClosesTheFilesItReads() {
    var sandbox = Directory.CreateTempSubdirectory().FullName;
    var source = Path.Combine(sandbox, "a.dfy");
    await File.WriteAllTextAsync(source, "lemma L(x: int) ensures x + 0 == x {}\n");
    var report = Path.Combine(sandbox, "report");

    await Dafny("verify", source, "--verification-coverage-report", report, "--no-timestamp-for-coverage-report");
    await Dafny("merge-coverage-reports", Path.Combine(sandbox, "merged"), report);

    // Throws while this process still has the file open; on Unix, .NET implements FileShare with flock.
    foreach (var file in new[] { source, Path.Combine(report, "index_verification.html"), Path.Combine(report, "a.dfy_verification.html") }) {
      new FileStream(file, FileMode.Open, FileAccess.Read, FileShare.None).Dispose();
    }
    Directory.Delete(sandbox, true);
  }

  private static async Task Dafny(params string[] args) {
    var output = new StringWriter();
    var exitCode = await DafnyBackwardsCompatibleCli.MainWithWriters(output, output, TextReader.Null, args);
    Assert.True(exitCode == 0, output.ToString());
  }
}
