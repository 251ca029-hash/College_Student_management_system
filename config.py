import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "college-sms-super-secret-key-2026")
    
    # Supabase PostgreSQL Settings
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
    
    # SQLite Fallback / Local Database
    SQLITE_DB_PATH = os.path.join(BASE_DIR, "college_sms.db")
    DATA_DIR = os.path.join(BASE_DIR, "data")
    
    # Pass thresholds
    MIN_ATTENDANCE_PCT = 75.0
    MIN_PASS_MARKS = 40.0
    MIN_EXTERNAL_PASS = 21.0
