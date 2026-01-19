import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Load .env
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

db_url = os.getenv("DATABASE_URL")
print(f"Testing connection to: {db_url}")

try:
    engine = create_engine(db_url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection successful! Result:", result.scalar())
except Exception as e:
    print(f"Connection failed: {e}")
