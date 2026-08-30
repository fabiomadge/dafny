global using Xunit;

// CoverageTalliesFileTest redirects the temp directory, which is process-wide, and the other tests
// here spawn children that inherit it. Two sibling test assemblies do the same.
[assembly: CollectionBehavior(DisableTestParallelization = true)]
