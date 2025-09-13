# Find all .ui files in assets/qtfile and Converted .py files output to src/gui directory

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
    return Find-ProjectRoot -currentDir $currentDir
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
# Use absolute path to specify uic tool
$uicPath = Join-Path -Path $projectRoot -ChildPath ".venv\Scripts\pyside6-uic.exe"

# Output path info for debugging
# Write-Host "Using UIC tool path: $uicPath"

# Check if uic tool exists
if (Test-Path -Path $uicPath) {
    # Check if ui file path parameters provided
    if ($args.Count -gt 0) {
        $uiFiles = $args
    } else {
        # Default to all .ui files in assets/qtfile directory
        $qtfileDir = Join-Path -Path $projectRoot -ChildPath "assets\qtfile"
        $uiFiles = Get-ChildItem -Path $qtfileDir -Filter "*.ui" | Select-Object -ExpandProperty FullName
        
        if ($uiFiles.Count -eq 0) {
            Write-Host "Error: No .ui files found in assets/qtfile directory" -ForegroundColor Red
            exit 1
        }
    }

    # Create output directory if not exists
    $outputDir = Join-Path -Path $projectRoot -ChildPath "src\gui"
    if (!(Test-Path -Path $outputDir)) {
        New-Item -Path $outputDir -ItemType Directory | Out-Null
        Write-Host "Created output directory: $outputDir" -ForegroundColor Green
    }

    # Convert all specified ui files
    $successCount = 0
    $failCount = 0
    
    foreach ($uiFile in $uiFiles) {
        # Check if ui file exists
        if (Test-Path -Path $uiFile) {
            # Build output file path
            $uiFileName = [System.IO.Path]::GetFileNameWithoutExtension($uiFile)
            $outputFile = Join-Path -Path $outputDir -ChildPath "${uiFileName}_ui.py"
            
            Write-Host "Converting $uiFile to $outputFile" -ForegroundColor Cyan
            
            # Run uic tool
            & $uicPath -o $outputFile $uiFile
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Convert success! Output file: $outputFile" -ForegroundColor Green
                $successCount++
            } else {
                Write-Host "Convert failed, error code: $LASTEXITCODE" -ForegroundColor Red
                $failCount++
            }
        } else {
            Write-Host "Error: ui file not found: $uiFile" -ForegroundColor Red
            $failCount++
        }
    }
    
    Write-Host "Conversion results summary:" -ForegroundColor Green
    Write-Host "Success: $successCount files" -ForegroundColor Green
    if ($failCount -ne 0) {
        Write-Host "Failed: $failCount files" -ForegroundColor Red
    }
} else {
    Write-Host "Error: pyside6-uic.exe not found, please ensure PySide6 is properly installed." -ForegroundColor Red
}

