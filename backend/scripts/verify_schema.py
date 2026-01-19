import os
import sys
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

inspector = inspect(engine)
tables = inspector.get_table_names()

required_tables = ['users', 'examens', 'lieux_examen', 'professeurs', 'etudiants', 'formations', 'modules']
missing_tables = [t for t in required_tables if t not in tables]

if missing_tables:
    print(f"MISSING TABLES: {missing_tables}")
    exit(1)
else:
    print(f"All required tables found: {tables}")
    exit(0)
