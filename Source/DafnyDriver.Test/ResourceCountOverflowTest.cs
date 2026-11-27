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
    results.OnNext(new CanVerifyResult(null!, ThreeExpensiveRuns()));
    results.OnCompleted();
    await summary;
  }

  private static List<VerificationTaskResult> ThreeExpensiveRuns() {
    return Enumerable.Range(0, 3).Select(vcNum =>
      new VerificationTaskResult(null!,
        new VerificationRunResult(vcNum, 0, DateTime.UnixEpoch, SolverOutcome.Valid,
          TimeSpan.Zero, 0, null!, new List<AssertCmd>(), new List<TrackedNodeComponent>(),
          PerRunResourceCount, null, new List<Microsoft.Boogie.Declaration>()))).ToList();
  }
}
