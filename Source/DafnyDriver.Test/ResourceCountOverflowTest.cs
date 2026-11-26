using System.Reactive.Subjects;
using DafnyDriver.Commands;
using Microsoft.Boogie;
using Microsoft.Dafny;
using VC;

namespace DafnyDriver.Test;

public class ResourceCountOverflowTest {

  private const int PerRunResourceCount = 800_000_000;
  private const long ExpectedTotal = 3L * PerRunResourceCount; // > int.MaxValue

  [Fact]
  public void TextLoggerReportsTotalWiderThanInt() {
    var writer = new StringWriter();
    TextVerificationLogger.LogResults(new ProofDependencyManager(), writer, ScopeWithThreeExpensiveRuns());
    Assert.Contains($"Overall resource count: {ExpectedTotal}", writer.ToString());
  }

  [Fact]
  public async Task JsonLoggerReportsTotalWiderThanInt() {
    var writer = new StringWriter();
    var logger = new JsonVerificationLogger(new ProofDependencyManager(), DafnyOptions.CreateUsingOldParser(writer).OutputWriter);
    logger.Initialize(new Dictionary<string, string>());
    logger.LogScopeResults(ScopeWithThreeExpensiveRuns());
    await logger.Flush();
    Assert.Contains($"\"resourceCount\":{ExpectedTotal}", writer.ToString());
  }

  [Fact]
  public async Task PerformanceStatisticsReportTotalWiderThanInt() {
    var writer = new StringWriter();
    var options = DafnyOptions.CreateUsingOldParser(writer);
    options.Set(VerifyCommand.PerformanceStatisticsOption, 1);
    await Summarize(VerifyCommand.ReportVerificationSummary, options);
    Assert.Contains($"Total resources used is {ExpectedTotal}", writer.ToString());
  }

  [Fact]
  public async Task MeasureComplexityReportsTotalWiderThanInt() {
    var writer = new StringWriter();
    await Summarize(MeasureComplexityCommand.ReportResourceSummary, DafnyOptions.CreateUsingOldParser(writer));
    Assert.Contains($"The total consumed resources are {ExpectedTotal}", writer.ToString());
  }

  private static async Task Summarize(Func<CliCompilation, IObservable<CanVerifyResult>, Task> report,
    DafnyOptions options) {
    var results = new Subject<CanVerifyResult>();
    var summary = report(CliCompilation.Create(options), results);
    results.OnNext(new CanVerifyResult(null!, ScopeWithThreeExpensiveRuns().Results));
    results.OnCompleted();
    await summary;
  }

  private static VerificationScopeResult ScopeWithThreeExpensiveRuns() {
    var results = Enumerable.Range(0, 3).Select(vcNum =>
      new VerificationTaskResult(null!,
        new VerificationRunResult(vcNum, 0, DateTime.UnixEpoch, SolverOutcome.Valid,
          TimeSpan.Zero, 0, null!, new List<AssertCmd>(), new List<TrackedNodeComponent>(),
          PerRunResourceCount, null, new List<Microsoft.Boogie.Declaration>()))).ToList();
    return new VerificationScopeResult(new VerificationScope("M", Microsoft.Boogie.Token.NoToken), results);
  }
}
