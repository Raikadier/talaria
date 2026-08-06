#Requires -Version 5.1
<#
.SYNOPSIS
  Finaliza el rename físico SkillGraph → Talaria.
  Quita el junction `Talaria` y renombra la carpeta real.
  Ejecutar con Cursor CERRADO sobre ese workspace (o deja este script esperando).
#>
$ErrorActionPreference = "Stop"
$parent = "D:\OneDrive - unicesar.edu.co\Business Ideas"
$real = Join-Path $parent "SkillGraph"
$alias = Join-Path $parent "Talaria"
$log = Join-Path $env:TEMP "talaria-rename-finalize.log"

function Write-Log([string]$msg) {
  $line = "{0:o} {1}" -f (Get-Date), $msg
  Add-Content -LiteralPath $log -Value $line
  Write-Host $line
}

Write-Log "START finalize rename"
Set-Location $env:TEMP

if (-not (Test-Path -LiteralPath $real)) {
  if ((Test-Path -LiteralPath $alias) -and -not ((Get-Item -LiteralPath $alias).Attributes -band [IO.FileAttributes]::ReparsePoint)) {
    Write-Log "Already renamed: Talaria is a real folder. OK"
    exit 0
  }
  Write-Log "ABORT: SkillGraph missing and Talaria not a real folder"
  exit 1
}

# Wait until rename is possible (Cursor lock)
$deadline = (Get-Date).AddHours(2)
while ((Get-Date) -lt $deadline) {
  try {
    $item = Get-Item -LiteralPath $alias -ErrorAction SilentlyContinue
    if ($null -ne $item -and ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
      [System.IO.Directory]::Delete($alias, $false)
      Write-Log "Removed junction Talaria"
    } elseif ($null -ne $item -and -not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
      Write-Log "Talaria already real folder; nothing to do"
      exit 0
    }

    Rename-Item -LiteralPath $real -NewName "Talaria" -ErrorAction Stop
    Write-Log "SUCCESS: renamed SkillGraph -> Talaria"
    Write-Log ("AGENTS.md exists: {0}" -f (Test-Path (Join-Path $alias "AGENTS.md")))
    exit 0
  } catch {
    Write-Log ("waiting for unlock: {0}" -f $_.Exception.Message)
    Start-Sleep -Seconds 5
  }
}

Write-Log "TIMEOUT after 2h — close Cursor and re-run"
exit 2
