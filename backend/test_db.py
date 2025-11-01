# backend/test_db.py
from database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        for row in result:
            print("✅ Connected to PostgreSQL successfully!")
            print("PostgreSQL version:", row[0])
except Exception as e:
    print("❌ Connection failed!")
    print(e)
