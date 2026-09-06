param(
    [Parameter(Mandatory=$true)]
    [string]$SourcePath,

    [string]$DestinationRelative = "archive/RepNet_V3_0_source"
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Source = (Resolve-Path $SourcePath).Path
$Destination = Join-Path $RepoRoot $DestinationRelative
$AuditDir = Join-Path $RepoRoot "migration_audit"

Write-Host "REP / RepNet V3 safe import preparation"
Write-Host "Source      : $Source"
Write-Host "Destination : $Destination"
Write-Host "Mode        : COPY ONLY / ORIGINAL SOURCE NOT MODIFIED"

$forbiddenDirectoryNames = @(
    ".venv", "venv", "env", "__pycache__", ".git", ".pytest_cache", ".mypy_cache",
    "memory", "memories", "state", "local_state", "persistent_state", "repnet_memory", "repnet_state",
    "cache", "tmp", "logs", "node_modules", "dist", "build"
)

$forbiddenExtensions = @(
    ".sqlite", ".sqlite3", ".db", ".duckdb", ".pkl", ".pickle", ".shelve", ".journal", ".wal",
    ".pt", ".pth", ".npy", ".npz", ".bin", ".pem", ".key", ".pfx", ".p12", ".log"
)

$allowedExtensions = @(
    ".py", ".ps1", ".json", ".toml", ".yaml", ".yml", ".md", ".txt", ".ini", ".cfg", ".csv"
)

if (Test-Path $Destination) {
    throw "Destination already exists: $Destination. Remove only the prepared copy after review, or choose another destination. The historical source is never modified by this script."
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null
New-Item -ItemType Directory -Force -Path $AuditDir | Out-Null

$copied = New-Object System.Collections.Generic.List[object]
$skipped = New-Object System.Collections.Generic.List[object]

$files = Get-ChildItem -LiteralPath $Source -File -Recurse -Force

foreach ($file in $files) {
    $relative = $file.FullName.Substring($Source.Length).TrimStart('\')
    $segments = $relative -split '[\\/]'
    $parentSegments = if ($segments.Count -gt 1) { $segments[0..($segments.Count-2)] } else { @() }
    $ext = $file.Extension.ToLowerInvariant()

    $reason = $null

    foreach ($segment in $parentSegments) {
        if ($forbiddenDirectoryNames -contains $segment) {
            $reason = "forbidden_directory:$segment"
            break
        }
    }

    if (-not $reason -and ($forbiddenExtensions -contains $ext)) {
        $reason = "forbidden_extension:$ext"
    }

    if (-not $reason -and ($file.Name -like ".env*" -or $file.Name -eq "config.json")) {
        $reason = "local_or_secret_config"
    }

    if (-not $reason -and -not ($allowedExtensions -contains $ext)) {
        $reason = "extension_not_allowlisted:$ext"
    }

    if ($reason) {
        $skipped.Add([pscustomobject]@{
            path = $relative
            bytes = $file.Length
            reason = $reason
        })
        continue
    }

    $target = Join-Path $Destination $relative
    $targetParent = Split-Path -Parent $target
    New-Item -ItemType Directory -Force -Path $targetParent | Out-Null
    Copy-Item -LiteralPath $file.FullName -Destination $target -Force

    $hash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash
    $copied.Add([pscustomobject]@{
        path = $relative
        bytes = $file.Length
        sha256 = $hash
    })
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$copiedCsv = Join-Path $AuditDir "repnet_v3_import_copied_$timestamp.csv"
$skippedCsv = Join-Path $AuditDir "repnet_v3_import_skipped_$timestamp.csv"
$summaryJson = Join-Path $AuditDir "repnet_v3_import_summary_$timestamp.json"

$copied | Sort-Object path | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $copiedCsv
$skipped | Sort-Object path | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $skippedCsv

$summary = [ordered]@{
    source_path = $Source
    destination_path = $Destination
    generated_utc = (Get-Date).ToUniversalTime().ToString("o")
    copied_file_count = $copied.Count
    skipped_file_count = $skipped.Count
    copied_total_bytes = (($copied | Measure-Object -Property bytes -Sum).Sum)
    skipped_total_bytes = (($skipped | Measure-Object -Property bytes -Sum).Sum)
    source_modified = $false
    persistent_memory_copied = $false
    policy = "ALLOWLISTED_TEXT_SOURCE_ONLY"
}

$summary | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $summaryJson

Write-Host ""
Write-Host "Safe import preparation complete."
Write-Host "Copied manifest : $copiedCsv"
Write-Host "Skipped manifest: $skippedCsv"
Write-Host "Summary         : $summaryJson"
Write-Host ""
Write-Host "IMPORTANT: Do not git add/commit yet. Review the prepared copy and audit files first."
