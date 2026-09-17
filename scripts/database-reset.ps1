$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot

Push-Location $repositoryRoot
try {
    & ".\.venv\Scripts\python.exe" -m alembic -c "services\incident-api\alembic.ini" downgrade base
    & ".\.venv\Scripts\python.exe" -m alembic -c "services\incident-api\alembic.ini" upgrade head
}
finally {
    Pop-Location
}

