# Define variables
$BUILD_DIR = "AeropressBuild"
$EXECUTABLES_DIR = "Executables"
$REPO_URL = "https://github.com/NikoLicht/BaristaCLI.git"
$PROJECT_NAME = "BaristaCLI"
$PYINSTALLER_FLAGS = "--onefile"
$MAIN_SCRIPT = "barista.py"

# Check if this is a fresh clone (no .git folder means it's not a repo)
if (Test-Path ".git") {
    # Check for unstaged or unpushed changes only if it's not a fresh clone
    $unstagedChanges = git status --porcelain | Select-String "^\s*M|^\s*D|^\s*A"
    $unpushedCommits = git log origin/main..HEAD --oneline

    if ($unstagedChanges -or $unpushedCommits) {
        Write-Host "WARNING: You have unstaged or unpushed changes!" -ForegroundColor Yellow
        Write-Host "Do you want to continue with the build? (y/n)"
        $confirmation = Read-Host
        if ($confirmation -ne "y") {
            Write-Host "Build aborted."
            exit
        }
    }
} else {
    Write-Host "Fresh clone detected. Skipping unstaged/unpushed changes check."
}

# Get the latest version number
$versionFile = "$EXECUTABLES_DIR\version.txt"

# Check if the version file exists
if (Test-Path $versionFile) {
    # Read the current version, clean it to ensure it's just a number
    $currentVersion = Get-Content $versionFile | Out-String
    $currentVersion = $currentVersion.Trim()  # Remove any extra whitespace or newline characters
    
    if ($currentVersion -match '^\d+$') {
        # Increment the version number if it's a valid integer
        $version = [int]$currentVersion + 1
    } else {
        Write-Host "ERROR: The version.txt file contains invalid data."
        exit 1
    }
} else {
    # If no version file exists, start at version 1
    $version = 1
}

# Set the executable file name with the new version
$exeName = "BaristaCLI_v$version.exe"

# Cleanup old build
if (Test-Path $BUILD_DIR) {
    Remove-Item -Recurse -Force $BUILD_DIR
}

# Clone fresh repo
git clone $REPO_URL $BUILD_DIR
Set-Location $BUILD_DIR

# Create virtual environment and activate it
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Build the executable
pyinstaller $PYINSTALLER_FLAGS --name $exeName --hidden-import=src.main $MAIN_SCRIPT

# Ensure Executables directory exists
Set-Location ..
if (!(Test-Path $EXECUTABLES_DIR)) {
    New-Item -ItemType Directory -Path $EXECUTABLES_DIR
}

# Move the built exe to Executables folder
Move-Item "$BUILD_DIR\dist\$exeName" "$EXECUTABLES_DIR"

# Save new version number
$version | Out-File $versionFile

# Cleanup build folder
Remove-Item -Recurse -Force $BUILD_DIR

Write-Host "Build complete! Executable saved to $EXECUTABLES_DIR\$exeName"

deactivate

