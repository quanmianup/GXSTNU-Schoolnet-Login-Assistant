<#
.SYNOPSIS
    GXSTNU Schoolnet Login Assistant - Main UI Packaging Script
.DESCRIPTION
    This script is used to package run.py into a single executable file with GUI interface.
    It automatically cleans up cache files after successful packaging and ensures AutoLoginScript.exe is included.
    Double-click this script to run the packaging process.
.NOTES
    File Name: build_main_ui.ps1
    Version: 1.0
    Author: Auto generated
    Encoding: UTF-8 with BOM
#>

# Set PowerShell execution policy to Bypass (only valid for current session)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Get project root directory (two levels up from current script location, since script is in src/tool directory)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Join-Path -Path $ScriptDir -ChildPath '..\..' -Resolve
$ProjectName = "GXSTNU-Schoolnet-Login-Assistant"
$SourceScript = "$ProjectRoot\run.py"
$DistDir = "$ProjectRoot\dist"
$BuildDir = "$ProjectRoot\build"
$SpecFile = "$ProjectRoot\$ProjectName.spec"
$IconFile = "$ProjectRoot\assets\images\main_icon.ico"
$AutoLoginScriptExe = "$DistDir\AutoLoginScript.exe"
$GenereLoginScript = "$ProjectRoot\src\tool\build_auto_login.ps1"
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

# Generate AutoLoginScript.exe if not exists
function Generate-AutoLoginScript {
    param()
    
    # Check and ensure AutoLoginScript.exe exists
    if (-not (Test-Path -Path $AutoLoginScriptExe)) {
        Write-Host "AutoLoginScript.exe not found. Generating it first..." -ForegroundColor Yellow
        
        if (Test-Path -Path $GenereLoginScript) {
            try {
                # Run build_auto_login.ps1 to generate AutoLoginScript.exe
                Push-Location -Path $ProjectRoot
                & "$GenereLoginScript"
                Pop-Location
                
                if (Test-Path -Path $AutoLoginScriptExe) {
                    Write-Host "AutoLoginScript.exe generated successfully." -ForegroundColor Green
                    return $true
                } else {
                    Write-Host "Failed to generate AutoLoginScript.exe" -ForegroundColor Red
                    return $false
                }
            } catch {
                Write-Host "Error: Failed to generate AutoLoginScript.exe: $_" -ForegroundColor Red
                return $false
            }
        } else {
            Write-Host "Error: build_auto_login.ps1 script not found." -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "AutoLoginScript.exe already exists, skipping generation." -ForegroundColor Green
        return $true
    }
}

# Main packaging function
function Invoke-Packaging {
    param()
    
    # Build PyInstaller command, including AutoLoginScript.exe as external resource
    $PyInstallerArgs = @(
        '--onefile',             # Generate single executable file
        '--windowed',            # Don't show console window (GUI application)
        '--log-level=WARN'
        "--name=$ProjectName", # Executable file name
        "--icon=$IconFile",     # Set application icon
        "--distpath=$DistDir",
        # Use --add-data parameter to include AutoLoginScript.exe as external resource
        "--add-data=$AutoLoginScriptExe;.\",
        # Add hidden imports to ensure all dependencies are included
        '--hidden-import=src.core.NetworkManager',
        '--hidden-import=src.utils.logger',
        '--hidden-import=src.core.TaskScheduler',
        '--hidden-import=src.core.Credentials',
        '--hidden-import=src.gui.main_gui_program',
        '--hidden-import=src.gui.main_ui',
        '--hidden-import=src.gui.window_rc',
        '--hidden-import=PySide6',
        '--hidden-import=PySide6.QtCore',
        '--hidden-import=PySide6.QtWidgets',
        '--hidden-import=requests',
        '--hidden-import=Crypto',
        '--hidden-import=loguru',
        "$SourceScript"
    )
    
    Write-Host "Packaging $SourceScript with PyInstaller..." -ForegroundColor Green
    Write-Host "Command: `npyinstaller $($PyInstallerArgs -join ' ')" -ForegroundColor Yellow
    
    try {
        # Change to project root directory to execute command
        Push-Location -Path $ProjectRoot
        Write-Host "`nPackaging process started..." -ForegroundColor Green
        pyinstaller $PyInstallerArgs
        Pop-Location
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "`nPackaging successful! Executable file generated at: $DistDir\$ProjectName.exe" -ForegroundColor Green
            return $true
        } else {
            Write-Host "`nPackaging failed with exit code: $LASTEXITCODE" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "Error: Problem occurred during packaging: $_" -ForegroundColor Red
        return $false
    }
}

# Main script execution
if (Test-Prerequisites) {
    $autoLoginGenerated = Generate-AutoLoginScript
    
    if ($autoLoginGenerated) {
        $packagingSuccess = Invoke-Packaging
        
        # Clean cache files if packaging was successful
        if ($packagingSuccess) {
            Remove-CacheFiles
        }
    }
}