import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "PropertyManagement.db")
PROMPTS_DIR = str(BASE_DIR / "app" / "prompts")
PHOTOS_DIR = str(BASE_DIR / "photos")
ISSUES_FILE = str(BASE_DIR / "issues.csv")
RESOLVED_ISSUES_FILE = str(BASE_DIR / "resolved_issues.csv")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "ADMIN")
