$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repositoryRoot ".venv\Scripts\python.exe"

Push-Location $repositoryRoot
try {
    & $python -m ruff check .
    & $python -m mypy services libs
    & $python -m pytest -q
    Push-Location "apps\web"
    try {
        npm run lint
        npm run typecheck
        npm run build
    }
    finally {
        Pop-Location
    }
}
finally {
    Pop-Location
}

