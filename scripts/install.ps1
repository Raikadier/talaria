#Requires -Version 5.1
<#
.SYNOPSIS
  Install Talaria on Windows (Python package + optional tools).
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
  powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1 -WithTools
#>
param(
  [switch]$WithTools,
  [switch]$SkipBoot
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location -LiteralPath $Root

Write-Host "Talaria root: $Root"
if ($PSVersionTable.PSVersion.Major -lt 5) { throw "PowerShell 5+ required" }

$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $py) { throw "Python >= 3.10 not found on PATH" }

& $py.Source -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)"
if ($LASTEXITCODE -ne 0) { throw "Python >= 3.10 required" }

$extras = if ($WithTools) { ".[tools]" } else { "." }
Write-Host "pip install -e $extras"
& $py.Source -m pip install -e $extras
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }

if (-not $SkipBoot) {
  Write-Host "talaria boot"
  & $py.Source -m talaria_cli boot
}

Write-Host ""
Write-Host "OK. Next:"
Write-Host "  talaria doctor --json"
Write-Host "  talaria connect --client cursor --json"
Write-Host "  Open this folder as an Obsidian vault (optional)"
Write-Host "  Set TALARIA_VAULT=$Root if you run from elsewhere"
