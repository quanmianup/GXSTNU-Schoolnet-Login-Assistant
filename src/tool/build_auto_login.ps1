<#
.SYNOPSIS
    GXSTNU Schoolnet Login Assistant - Auto Packaging Script
.DESCRIPTION
    This script is used to package AutoLoginScript.py into a single executable file with console output logs
    Double-click this script to run the packaging process
.NOTES
    File Name: build_auto_login.ps1
    Version: 1.5
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
$SourceScript = "$ProjectRoot\src\core\AutoLoginScript.py"
$DistDir = "$ProjectRoot\dist"
$BuildDir = "$ProjectRoot\build"
$SpecFile = "$ProjectRoot\AutoLoginScript.spec"
# 使用绝对路径引用图标文件，避免路径解析问题
$IconFile = Join-Path -Path $ProjectRoot -ChildPath "assets\images\main_icon.ico"

# 确保输出目录存在
if (-not (Test-Path -Path $DistDir)) {
    New-Item -Path $DistDir -ItemType Directory -Force | Out-Null
}

# 构建PyInstaller命令
$PyInstallerArgs = @(
    '--onefile',             # 生成单个可执行文件
    '--console',             # 显示控制台窗口，用于输出日志
    '--name=AutoLoginScript', # 可执行文件名称
    "--icon=$IconFile",     # 设置应用图标，使用引号包裹整个参数
    "--distpath=$DistDir",
    "--workpath=$BuildDir",
    # 添加隐藏的导入以确保所有依赖都被包含
    '--hidden-import=src.core.NetworkManager',
    '--hidden-import=src.utils.logger',
    '--hidden-import=requests',
    '--hidden-import=pycryptodome',
    '--hidden-import=loguru',
    "$SourceScript"
)

Write-Host "Packaging with PyInstaller..." -ForegroundColor Green
Write-Host "Command: pyinstaller $($PyInstallerArgs -join ' ')" -ForegroundColor Yellow

# 执行PyInstaller命令
try {
    # 切换到项目根目录执行命令
    Push-Location -Path $ProjectRoot
    pyinstaller $PyInstallerArgs
    Pop-Location
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nPackaging successful! Executable file generated at: $DistDir" -ForegroundColor Green
        Write-Host "Note: When running the generated exe file, the console will display log output." -ForegroundColor Cyan
        
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