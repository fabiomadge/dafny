using Microsoft.Dafny;
using Microsoft.Dafny.Compilers;

namespace DafnyCore.Test;

public class ExecutableBackendTest {

  [Fact]
  public void WriteFromFileClosesTheFile() {
    var file = Path.GetTempFileName();
    Backend.WriteFromFile(file);
    // Not Windows-only: on Unix, .NET implements FileShare with flock.
    new FileStream(file, FileMode.Open, FileAccess.Read, FileShare.None).Dispose();
    File.Delete(file);
  }

  [Fact]
  public async Task WaitForExitClosesThePipesItDrains() {
    var backend = new Backend();
    using var process = backend.StartProcess(backend.PrepareProcessStartInfo("dotnet", ["--version"]), TextWriter.Null);
    await backend.WaitForExit(process, TextWriter.Null, TextWriter.Null);
    Assert.Throws<ObjectDisposedException>(() => process.StandardOutput.Peek());
    Assert.Throws<ObjectDisposedException>(() => process.StandardError.Peek());
  }

  private class Backend() : JavaScriptBackend(new DafnyOptions(TextReader.Null, TextWriter.Null, TextWriter.Null)) {
    public static void WriteFromFile(string path) => WriteFromFile(path, TextWriter.Null);
  }
}
