# Local development

## Prerequisites

- Python 3.14.x
- Node.js 24.x and npm 11.x

## First setup

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e '.[dev]'
Set-Location apps\web
npm install
Copy-Item .env.local.example .env.local
Set-Location ..\..
```

## Run

Run both processes in hidden background windows:

```powershell
.\scripts\run-local.ps1
```

Or run them in separate terminals using the commands in each component README. Open:

- Web: `http://localhost:3000`
- Incident API documentation: `http://localhost:8000/docs`
- Incident API health: `http://localhost:8000/health/ready`

Requests are intentionally in memory for Phase 1 and disappear when the API restarts.

## Verify

```powershell
.\scripts\verify-phase-1.ps1
```

