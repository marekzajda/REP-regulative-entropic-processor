param(
    [int]$IntervalSeconds = 300,
    [switch]$Once
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $RepoRoot

function Invoke-REPConnectorCycle {
    Write-Host "[$(Get-Date -Format s)] REP connector cycle"

    git pull --ff-only
    if ($LASTEXITCODE -ne 0) { throw "git pull failed" }

    python connector/rep_connector.py --once
    $connectorCode = $LASTEXITCODE

    git add jobs/processed jobs/failed results
    $changes = git status --porcelain
    if ($changes) {
        git commit -m "REP connector: collect local run results"
        if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
        git push
        if ($LASTEXITCODE -ne 0) { throw "git push failed" }
    }

    return $connectorCode
}

if ($Once) {
    exit (Invoke-REPConnectorCycle)
}

while ($true) {
    try {
        Invoke-REPConnectorCycle | Out-Null
    }
    catch {
        Write-Error $_
    }
    Start-Sleep -Seconds $IntervalSeconds
}
