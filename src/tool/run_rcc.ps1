# Find all .qrc files in assets\qtfile and Converted .py files output to src\gui directory

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
if (Test-Path -Path  $projectRoot) {
} else {
    Write-Host "Error: Project root not found, tool path." -ForegroundColor Red
    exit 1
}


# Use absolute path to specify rcc tool
$rccPath = Join-Path -Path $projectRoot -ChildPath ".venv\Scripts\pyside6-rcc.exe"

# Output path info for debugging
# Write-Host "Using RCC tool path: $rccPath"

# Check if rcc tool exists
if (Test-Path -Path $rccPath) {
    # Check if qrc file path parameters provided
    if ($args.Count -gt 0) {
        $qrcFiles = $args
    } else {
        # Default to all .qrc files in assets/qtfile directory
        $qtfileDir = Join-Path -Path $projectRoot -ChildPath "assets\qtfile"
        $qrcFiles = Get-ChildItem -Path $qtfileDir -Filter "*.qrc" | Select-Object -ExpandProperty FullName
        
        if ($qrcFiles.Count -eq 0) {
            Write-Host "Error: No .qrc files found in assets/qtfile directory" -ForegroundColor Red
            exit 1
        }
        $qrcFiles | ForEach-Object { Write-Host "  - $_" }
    }

    # Create output directory if not exists
    $outputDir = Join-Path -Path $projectRoot -ChildPath "src\gui"
    if (!(Test-Path -Path $outputDir)) {
        New-Item -Path $outputDir -ItemType Directory | Out-Null
        Write-Host "Created output directory: $outputDir"
    }

    # Convert all specified qrc files
    $successCount = 0
    $failCount = 0
    
    foreach ($qrcFile in $qrcFiles) {
        # Check if qrc file exists
        if (Test-Path -Path $qrcFile) {
            # Build output file path
            $qrcFileName = [System.IO.Path]::GetFileNameWithoutExtension($qrcFile)
            $outputFile = Join-Path -Path $outputDir -ChildPath "${qrcFileName}_rc.py"
            
            Write-Host "Converting $qrcFile to $outputFile" -ForegroundColor Cyan
            
            # Run rcc tool
            & $rccPath -o $outputFile $qrcFile
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Convert success! Output file: $outputFile" -ForegroundColor Green
                $successCount++
            } else {
                Write-Host "Convert failed, error code: $LASTEXITCODE" -ForegroundColor Red
                $failCount++
            }
        } else {
            Write-Host "Error: qrc file not found: $qrcFile" -ForegroundColor Red
            $failCount++
        }
    }
    
    Write-Host "Conversion results summary:" -ForegroundColor Green
    Write-Host "Success: $successCount files" -ForegroundColor Green
    if ($failCount -gt 0) {
        Write-Host "Failed: $failCount files" -ForegroundColor Red
    }
} else {
    Write-Host "Error: pyside6-rcc.exe not found, please ensure PySide6 is properly installed." -ForegroundColor Red
}