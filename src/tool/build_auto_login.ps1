<#
.SYNOPSIS
    GXSTNU Schoolnet Login Assistant - Auto Packaging Script
.DESCRIPTION
    This script is used to package AutoLoginScript.py into a single executable file with console output logs.
    It automatically cleans up cache files after successful packaging.
    Double-click this script to run the packaging process.
.NOTES
    File Name: build_auto_login.ps1
    Version: 1.0
    Author: Auto generated
    Encoding: UTF-8 with BOM
#>

# Set PowerShell execution policy to Bypass (only valid for current session)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Get project root directory (two levels up from current script location, since script is in src/tool directory)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Join-Path -Path $ScriptDir -ChildPath '..\..' -Resolve

# Define packaging parameters
$SourceScript = "$ProjectRoot\src\core\AutoLoginScript.py"
$DistDir = "$ProjectRoot\dist"
$BuildDir = "$ProjectRoot\build"
$SpecFile = "$ProjectRoot\AutoLoginScript.spec"
$IconFile = "$ProjectRoot\assets\images\main_icon.ico"

# Function to clean up cache files
function Remove-CacheFiles {
    param()
    
    Write-Host "`nCleaning up cache files..." -ForegroundColor Green
    
    Remove-Item -Path $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path $SpecFile -Force -ErrorAction SilentlyContinue
    
    Write-Host "Cache files cleaned up successfully." -ForegroundColor Green
}

# Check prerequisites
function Test-Prerequisites {
    param()
    
    # Check if running in virtual environment
    $VenvPath = "$ProjectRoot\.venv"
    if (-not (Test-Path -Path $VenvPath)) {
        Write-Host "Warning: It is recommended to run this packaging script in a virtual environment." -ForegroundColor Yellow
    }
    
    # Check if pyinstaller is installed
    try {
        Get-Command -Name 'pyinstaller' -ErrorAction Stop | Out-Null
        return $true
    } catch {
        Write-Host "Error: pyinstaller executable not found, please install pyinstaller first." -ForegroundColor Red
        Write-Host "Please run: uv pip install pyinstaller" -ForegroundColor Yellow
        return $false
    }
}

# Main packaging function
function Invoke-Packaging {
    param()
    
    # Build PyInstaller command
    $PyInstallerArgs = @(
        '--onefile',         
        '--console',      
        '--clean',
        '--name=AutoLoginScript',
        "--icon=$IconFile",
        '--log-level=WARN',
        '--hidden-import=src.core.NetworkManager',
        '--hidden-import=src.utils.logger',
        '--hidden-import=requests',
        '--hidden-import=Crypto',
        '--hidden-import=loguru',
        "$SourceScript"
    )
    
    Write-Host "Packaging $SourceScript with PyInstaller..." -ForegroundColor Green
    Write-Host "Command:`npyinstaller $($PyInstallerArgs -join ' ')" -ForegroundColor Yellow
    
    try {
        # Change to project root directory to execute command
        Push-Location -Path $ProjectRoot
        
        Write-Host "Packaging Now... " -ForegroundColor Cyan
        # Use Start-Process for more reliable execution
        $ProcessInfo = Start-Process -FilePath 'pyinstaller' -ArgumentList $PyInstallerArgs -NoNewWindow -Wait -PassThru
        Pop-Location
        
        if ($ProcessInfo.ExitCode -eq 0) {
            Write-Host "`nPackaging successful! Generated file: $DistDir\AutoLoginScript.exe" -ForegroundColor Green
            return $true
        } else {
            Write-Host "`nPackaging failed with exit code: $($ProcessInfo.ExitCode)" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "Error: Problem occurred during packaging: $_" -ForegroundColor Red
        return $false
    }
}

# Main script execution
if (Test-Prerequisites) {
    $packagingSuccess = Invoke-Packaging
    
    # Clean cache files regardless of packaging success
    if ($packagingSuccess) {
        Remove-CacheFiles
    }
}