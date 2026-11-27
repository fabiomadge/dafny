using System.Text.Json.Nodes;
using Microsoft.Boogie;
using Microsoft.Dafny;
using VC;

namespace DafnyDriver.Test;

public class VerificationLoggerResourceCountTest {
  private const long ExpectedTotal = (long)int.MaxValue + 1;

  [Fact]
  public void TextLoggerReportsTotalWiderThanInt() {
    var output = new StringWriter();
    TextVerificationLogger.LogResults(new ProofDependencyManager(), output, CreateScopeResult(int.MaxValue, 1));
    Assert.Contains($"Overall resource count: {ExpectedTotal}", output.ToString());
  }

  [Fact]
  public async Task JsonLoggerReportsTotalWiderThanInt() {
    var output = new StringWriter();
    var logger = new JsonVerificationLogger(new ProofDependencyManager(),
      new DafnyOptions(TextReader.Null, output, TextWriter.Null).OutputWriter);
    logger.Initialize(new Dictionary<string, string>());
    logger.LogScopeResults(CreateScopeResult(int.MaxValue, 1));
    await logger.Flush();
    var scope = JsonNode.Parse(output.ToString())!["verificationResults"]![0]!;
    Assert.Equal(ExpectedTotal, scope["resourceCount"]!.GetValue<long>());
  }

  private static VerificationScopeResult CreateScopeResult(params int[] resourceCounts) {
    var results = resourceCounts.Select((resourceCount, index) => new VerificationTaskResult(null!,
      new VerificationRunResult(index + 1, 0, DateTime.UnixEpoch, SolverOutcome.Valid, TimeSpan.Zero,
        0, null!, new List<AssertCmd>(), new List<TrackedNodeComponent>(), resourceCount, null,
        new List<Microsoft.Boogie.Declaration>()))).ToList();
    return new VerificationScopeResult(new VerificationScope("M", Microsoft.Boogie.Token.NoToken), results);
  }
}
