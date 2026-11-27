using System.Text.Json.Nodes;
using Microsoft.Boogie;
using Microsoft.Dafny;
using VC;
using Token = Microsoft.Dafny.Token;

namespace DafnyDriver.Test;

public class VerificationLoggerResourceCountTest {
  [Fact]
  public void TextLoggerReportsTotalWiderThanInt() {
    using var output = new StringWriter();
    TextVerificationLogger.LogResults(new ProofDependencyManager(), output, CreateScopeResult(int.MaxValue, 1));

    Assert.Contains($"  Overall resource count: 2147483648{Environment.NewLine}", output.ToString());
  }

  [Fact]
  public async Task JsonLoggerReportsTotalWiderThanInt() {
    using var output = new StringWriter();
    var options = new DafnyOptions(TextReader.Null, output, TextWriter.Null);
    var logger = new JsonVerificationLogger(new ProofDependencyManager(), options.OutputWriter);
    logger.Initialize(new Dictionary<string, string>());

    logger.LogScopeResults(CreateScopeResult(int.MaxValue, 1));
    await logger.Flush();

    var log = JsonNode.Parse(output.ToString())!;
    var scope = Assert.Single(log["verificationResults"]!.AsArray())!;
    Assert.Equal(2147483648L, scope["resourceCount"]!.GetValue<long>());
  }

  private static VerificationScopeResult CreateScopeResult(params int[] resourceCounts) {
    var results = resourceCounts.Select((resourceCount, index) => new VerificationTaskResult(null!,
      new VerificationRunResult(index + 1, 0, DateTime.UnixEpoch, SolverOutcome.Valid, TimeSpan.Zero,
        0, null!, new List<AssertCmd>(), new List<TrackedNodeComponent>(), resourceCount, null,
        new List<Microsoft.Boogie.Declaration>()))).ToList();
    return new VerificationScopeResult(new VerificationScope("M", Token.NoToken), results);
  }
}
