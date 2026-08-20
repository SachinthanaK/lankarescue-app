$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repositoryRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python)) {
    throw "Python environment is missing. Follow docs/local-development.md first."
}

Start-Process -FilePath $python -WindowStyle Hidden -WorkingDirectory $repositoryRoot -ArgumentList @(
    "-m", "uvicorn", "incident_api.main:app",
    "--app-dir", "services/incident-api/src",
    "--reload", "--port", "8000"
)

Start-Process -FilePath "npm.cmd" -WindowStyle Hidden -WorkingDirectory (Join-Path $repositoryRoot "apps\web") -ArgumentList @("run", "dev")

Write-Host "Incident API: http://localhost:8000/docs"
Write-Host "Web application: http://localhost:3000"

