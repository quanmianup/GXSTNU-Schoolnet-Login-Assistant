# This script starts Qt Designer
function Find-ProjectRoot {
    param (
        [string]$currentDir
    )
    # Check if current directory contains pyproject.toml
    $pyprojectPath = Join-Path -Path $currentDir -ChildPath "pyproject.toml"
    if (Test-Path -Path $pyprojectPath) {
        return $currentDir
    }
    
    # Get parent directory
    $parentDir = Split-Path -Parent $currentDir
    
    # Stop searching if reached root directory
    if ($parentDir -eq $currentDir) {
        Write-Host "Error: pyproject.toml not found, cannot determine project root." -ForegroundColor Red
        return $null
    }
    
    # Recursively search parent directory
    return Find-ProjectRoot -currentDir $parentDir
}

# Get current working directory
$currentDir = Get-Location

# Find project root directory
$projectRoot = Find-ProjectRoot -currentDir $currentDir

# Continue execution if project root is found
if (Test-Path -Path  $projectRoot) {
} else {
    Write-Host "Error: Project root not found, cannot determine tool path." -ForegroundColor Red
    exit 1
}
# Use absolute path to specify designer tool
$designerPath = Join-Path -Path $projectRoot -ChildPath ".venv\Scripts\pyside6-designer.exe"

# Check if designer tool exists
if (Test-Path -Path $designerPath) {
    # Start designer tool
    Write-Host "Executing: '$designerPath'" -ForegroundColor Green
    
    # Start designer tool (async, non-blocking)
    Start-Process -FilePath $designerPath -WindowStyle Hidden
    
    # Check if started successfully (simple check due to async start)
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Qt Designer started successfully!" -ForegroundColor Green
        Write-Host "After design, save .ui files to assets/qtfile directory, then use run_uic.ps1 to convert to Python files." -ForegroundColor Cyan
    } else {
        Write-Host "Start failed, error code: $LASTEXITCODE" -ForegroundColor Red
    }
} else {
    Write-Host "Error: pyside6-designer.exe not found, please ensure PySide6 is properly installed." -ForegroundColor Red
}
