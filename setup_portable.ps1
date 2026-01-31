# Powershell Script to set up Portable Python
$workdir = Get-Location
$pythonDir = "$workdir\python_env"
$zipPath = "$workdir\python.zip"
$url = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-embed-amd64.zip"

Write-Host "1. Creating local Python environment..."
if (Test-Path $pythonDir) {
    Write-Host "   Existing python_env found."
} else {
    New-Item -ItemType Directory -Force -Path $pythonDir | Out-Null
    
    Write-Host "2. Downloading Python 3.11 Embeddable..."
    Invoke-WebRequest -Uri $url -OutFile $zipPath
    
    Write-Host "3. Extracting Python..."
    Expand-Archive -Path $zipPath -DestinationPath $pythonDir -Force
    Remove-Item $zipPath
}

# Enable pip in embedded python (uncomment import site)
$pthFile = "$pythonDir\python311._pth"
if (Test-Path $pthFile) {
    $content = Get-Content $pthFile
    $content = $content -replace "#import site", "import site"
    Set-Content $pthFile $content
    Write-Host "4. Configured python._pth for pip support."
}

# Download get-pip
$getPipPath = "$pythonDir\get-pip.py"
if (-not (Test-Path "$pythonDir\Scripts\pip.exe")) {
    Write-Host "5. Downloading pip bootstrapper..."
    Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $getPipPath
    
    Write-Host "6. Installing pip..."
    & "$pythonDir\python.exe" $getPipPath
    Remove-Item $getPipPath
}

Write-Host "7. Installing requirements..."
& "$pythonDir\python.exe" -m pip install -r requirements.txt

Write-Host "DONE! Portable Python is ready."
Start-Sleep -Seconds 2
