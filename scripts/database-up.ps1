$ErrorActionPreference = "Stop"
$repositoryRoot = Split-Path -Parent $PSScriptRoot

Push-Location $repositoryRoot
try {
    docker compose up -d postgres
    docker compose ps postgres
    & ".\.venv\Scripts\python.exe" -m alembic -c "services\incident-api\alembic.ini" upgrade head
}
finally {
    Pop-Location
}

