#!/bin/bash
# Run this checkout's Dafny CLI (Binaries/Dafny.dll, from `dotnet build Source/Dafny/Dafny.csproj`).
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PATH="$HOME/.dotnet:$PATH"
exec dotnet "${DAFNY_DLL:-$HERE/../../Binaries/Dafny.dll}" "$@"
