# Kazmiskender WMS

A modular warehouse management system implemented with PySide6 and SQLAlchemy.

## Features

- Inventory, purchasing, invoicing, reporting, and user management modules
- Qt Designer generated UI with repository-driven CRUD actions
- ReportLab PDF invoice generation and pandas Excel export
- Role-based access control with SQLite persistence
- Alembic migrations and pytest-powered automated tests
- GitHub Actions CI pipeline and PyInstaller build configuration for Windows and Linux

## Getting started

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install --upgrade pip
pip install -e .[dev]
```

### Initialize the database

```bash
alembic upgrade head
python -m app.scripts.seed_data
```

### Launch the application

```bash
python -m app
```

### Running tests

```bash
pytest
```

### Generate distributables

#### Windows executable

```bash
pyinstaller pyinstaller.spec
```

#### Linux AppImage

```bash
./scripts/build_appimage.sh
```

The AppImage script uses `linuxdeploy` to bundle the PySide6 runtime.

## Continuous integration

The project is configured with GitHub Actions (`.github/workflows/ci.yml`) to run pytest on every push and pull request.

## Release notes

### v0.1.0

- Initial module scaffolding (inventory, purchasing, invoicing, reports, users)
- Qt Designer UI forms converted with `pyside6-uic`
- Repository pattern built on SQLAlchemy sessions
- Invoice PDF generation with ReportLab
- Excel reporting via pandas + openpyxl
- User authentication and role-based menu enablement
- PyInstaller specs for Windows/Linux builds and AppImage helper script
