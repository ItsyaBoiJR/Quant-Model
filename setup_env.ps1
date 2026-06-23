# Setup script for Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Environment setup complete. To activate in the future, run: .\venv\Scripts\Activate.ps1"
