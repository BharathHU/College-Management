import os
import subprocess
import sys
from pathlib import Path


# Tests use a fresh ignored SQLite fixture created by the same Alembic migration; deployments use MySQL via DATABASE_URL.
database_path = Path(__file__).resolve().parents[1] / "test.db"
if database_path.exists():
	database_path.unlink()
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"], cwd=database_path.parent, check=True)

from app.seed import seed

seed()