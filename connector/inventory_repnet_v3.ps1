param(
    [Parameter(Mandatory=$true)]
    [string]$SourcePath,

    [string]$OutDir = ".\inventory_out"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $SourcePath)) {
    throw "Source path not found: $SourcePath"
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$manifestCsv = Join-Path $OutDir "repnet_v3_manifest.csv"
$summaryJson = Join-Path $OutDir "repnet_v3_inventory_summary.json"
$treeTxt = Join-Path $OutDir "repnet_v3_tree.txt"

# Read-only inventory. This script never starts RepNet, Ollama, Python or Uvicorn.
$files = Get-ChildItem -LiteralPath $SourcePath -Recurse -File -Force

$records = foreach ($f in $files) {
    $rel = $f.FullName.Substring($SourcePath.TrimEnd('\\').Length).TrimStart('\\')
    $hash = Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256

    [PSCustomObject]@{
        relative_path = $rel
        size_bytes = $f.Length
        modified_utc = $f.LastWriteTimeUtc.ToString("o")
        sha256 = $hash.Hash.ToLowerInvariant()
        extension = $f.Extension.ToLowerInvariant()
    }
}

$records | Sort-Object relative_path | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $manifestCsv

$records.relative_path | Sort-Object | Set-Content -Encoding UTF8 -Path $treeTxt

$known = [ordered]@{
    brain_server = Test-Path -LiteralPath (Join-Path $SourcePath "brain_server.py")
    adapter_chat = Test-Path -LiteralPath (Join-Path $SourcePath "adapter_chat.py")
    repnet_state = Test-Path -LiteralPath (Join-Path $SourcePath "memory\repnet_state.npz")
    memory_sqlite = Test-Path -LiteralPath (Join-Path $SourcePath "memory\memory.sqlite")
    readout_head = Test-Path -LiteralPath (Join-Path $SourcePath "memory\readout_head.pt")
    venv = Test-Path -LiteralPath (Join-Path $SourcePath ".venv")
}

$summary = [ordered]@{
    source_path = $SourcePath
    generated_utc = (Get-Date).ToUniversalTime().ToString("o")
    file_count = $records.Count
    total_bytes = ($records | Measure-Object -Property size_bytes -Sum).Sum
    known_components = $known
    safety = "READ_ONLY_INVENTORY_NO_RUNTIME_EXECUTION"
}

$summary | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 -Path $summaryJson

Write-Host "Inventory complete."
Write-Host "Manifest: $manifestCsv"
Write-Host "Summary : $summaryJson"
Write-Host "Tree    : $treeTxt"
