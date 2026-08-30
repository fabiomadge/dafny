global using Xunit;

// CoverageTalliesFileTest redirects the temp directory, which is process-wide, and the other tests
// here spawn child processes that inherit it. Two sibling assemblies do the same for the same
// reason; nothing in this one is fast enough for the parallelism to be worth the interference.
[assembly: CollectionBehavior(DisableTestParallelization = true)]
