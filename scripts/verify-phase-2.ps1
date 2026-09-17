$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repositoryRoot ".venv\Scripts\python.exe"

Push-Location $repositoryRoot
try {
    & $python -m ruff check .
    & $python -m mypy services libs
    & $python -m pytest -q
    $env:RUN_POSTGRES_TESTS = "1"
    & $python -m pytest -q -m integration
    & $python -m alembic -c "services\incident-api\alembic.ini" downgrade base
    & $python -m alembic -c "services\incident-api\alembic.ini" upgrade head
}
finally {
    Remove-Item Env:\RUN_POSTGRES_TESTS -ErrorAction SilentlyContinue
    Pop-Location
}

