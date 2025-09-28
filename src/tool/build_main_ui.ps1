<#
.SYNOPSIS
    GXSTNU Schoolnet Login Assistant - Main UI Packaging Script
.DESCRIPTION
    This script is used to package run.py into a single executable file with GUI interface
    Double-click this script to run the packaging process
.NOTES
    File Name: build_main_ui.ps1
    Version: 1.0
    Author: Auto generated
    Encoding: UTF-8 with BOM
#>

# Skip encoding settings to avoid issues

# Set PowerShell execution policy to Bypass (only valid for current session)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# 获取项目根目录（从当前脚本位置向上两级，因为脚本在src/tool目录下）
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Join-Path -Path $ScriptDir -ChildPath '..\..'
$ProjectRoot = Resolve-Path $ProjectRoot

# Check if running in virtual environment
$VenvPath = "$ProjectRoot\.venv"
if (-not (Test-Path -Path $VenvPath)) {
    Write-Host "Warning: It is recommended to run this packaging script in a virtual environment." -ForegroundColor Yellow
}

# Check if pyinstaller is installed
try {
    Get-Command -Name 'pyinstaller' -ErrorAction Stop | Out-Null
} catch {
    Write-Host "Error: pyinstaller executable not found, please install pyinstaller first." -ForegroundColor Red
    Write-Host "Please run: uv pip install pyinstaller" -ForegroundColor Yellow
    Read-Host "Press Enter to exit..."
    exit 1
}

# 定义打包参数
$SourceScript = "$ProjectRoot\run.py"
$DistDir = "$ProjectRoot\dist"
$BuildDir = "$ProjectRoot\build"
$SpecFile = "$ProjectRoot\GXSTNU_Schoolnet_Login.spec"
# 使用绝对路径引用图标文件，避免路径解析问题
$IconFile = Join-Path -Path $ProjectRoot -ChildPath "assets\images\main_icon.ico"

# 定义AutoLoginScript.exe路径
$AutoLoginScriptExe = Join-Path -Path $DistDir -ChildPath "AutoLoginScript.exe"

# 确保输出目录存在
if (-not (Test-Path -Path $DistDir)) {
    New-Item -Path $DistDir -ItemType Directory -Force | Out-Null
}

# 检查并确保AutoLoginScript.exe存在
if (-not (Test-Path -Path $AutoLoginScriptExe)) {
    Write-Host "AutoLoginScript.exe not found. Generating it first..." -ForegroundColor Yellow
    $BuildAutoLoginScript = Join-Path -Path $ProjectRoot -ChildPath "src\tool\build_auto_login.ps1"
    
    if (Test-Path -Path $BuildAutoLoginScript) {
        try {
            # 运行build_auto_login.ps1生成AutoLoginScript.exe
            Push-Location -Path $ProjectRoot
            & "$BuildAutoLoginScript"
            Pop-Location
            
            if (-not (Test-Path -Path $AutoLoginScriptExe)) {
                throw "Failed to generate AutoLoginScript.exe"
            }
        } catch {
            Write-Host "Error: Failed to generate AutoLoginScript.exe: $_" -ForegroundColor Red
            Read-Host "Press Enter to exit..."
            exit 1
        }
    } else {
        Write-Host "Error: build_auto_login.ps1 script not found." -ForegroundColor Red
        Read-Host "Press Enter to exit..."
        exit 1
    }
}

# 构建PyInstaller命令，包含AutoLoginScript.exe作为外部资源
$PyInstallerArgs = @(
    '--onefile',             # 生成单个可执行文件
    '--windowed',            # 不显示控制台窗口（GUI应用）
    '--name=GXSTNU_Schoolnet_Login', # 可执行文件名称
    "--icon=$IconFile",     # 设置应用图标，使用引号包裹整个参数
    "--distpath=$DistDir",
    "--clean",              # Clean PyInstaller cache and remove temporary files before building.
    # 使用--add-data参数将AutoLoginScript.exe作为外部资源包含
    "--add-data=$AutoLoginScriptExe;.\",
    # 添加隐藏的导入以确保所有依赖都被包含
    '--hidden-import=src.core.NetworkManager',
    '--hidden-import=src.utils.logger',
    '--hidden-import=src.core.TaskScheduler',
    '--hidden-import=src.core.Credentials',
    '--hidden-import=src.gui.main_gui_program',
    '--hidden-import=src.gui.main_ui',
    '--hidden-import=PySide6',
    '--hidden-import=PySide6.QtCore',
    '--hidden-import=PySide6.QtWidgets',
    '--hidden-import=requests',
    '--hidden-import=Crypto',
    '--hidden-import=loguru',
    "$SourceScript"
)

Write-Host "Packaging Main UI with PyInstaller..." -ForegroundColor Green
Write-Host "Command: pyinstaller $($PyInstallerArgs -join ' ')" -ForegroundColor Yellow

# 执行PyInstaller命令
try {
    # 切换到项目根目录执行命令
    Push-Location -Path $ProjectRoot
    pyinstaller $PyInstallerArgs
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nPackaging successful! Executable file generated at: $DistDir\GXSTNU_Schoolnet_Login.exe" -ForegroundColor Green
        Write-Host "Note: This is the main GUI application of GXSTNU Schoolnet Login Assistant." -ForegroundColor Cyan
        
        # Clean up temporary files
        Write-Host "`nCleaning up temporary files..." -ForegroundColor Green
        
        # Delete build directory
        if (Test-Path -Path $BuildDir -PathType Container) {
            Write-Host "Deleting build directory: $BuildDir" -ForegroundColor Yellow
            Remove-Item -Path $BuildDir -Recurse -Force
        }
        
        # Delete spec file
        if (Test-Path -Path $SpecFile -PathType Leaf) {
            Write-Host "Deleting spec file: $SpecFile" -ForegroundColor Yellow
            Remove-Item -Path $SpecFile -Force
        }
        
        Write-Host "Temporary files cleaned up." -ForegroundColor Green
    } else {
        throw "PyInstaller execution failed, exit code: $LASTEXITCODE"
    }
} catch {
    Write-Host "Error: Problem occurred during packaging: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

# Prompt user that packaging is complete
Read-Host "Packaging process completed, press Enter to exit..."