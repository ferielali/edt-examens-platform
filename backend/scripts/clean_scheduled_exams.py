# -*- coding: utf-8 -*-
"""Clean existing scheduled exams and test generation"""
import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

# Delete existing scheduled exams with status 'scheduled' to clean up
with engine.connect() as conn:
    # First check what we have
    result = conn.execute(text("""
        SELECT statut, COUNT(*) as count 
        FROM examens 
        GROUP BY statut
    """))
    print("Current exam status counts:")
    for row in result:
        print(f"  - {row.statut}: {row.count}")
    
    # Delete scheduled exams that were auto-generated (have session_id)
    deleted = conn.execute(text("""
        DELETE FROM examens 
        WHERE statut = 'scheduled' AND session_id IS NOT NULL
        RETURNING id
    """))
    deleted_count = len(deleted.fetchall())
    conn.commit()
    print(f"\nDeleted {deleted_count} auto-generated scheduled exams")
    
    # Check again
    result = conn.execute(text("""
        SELECT statut, COUNT(*) as count 
        FROM examens 
        GROUP BY statut
    """))
    print("\nAfter cleanup:")
    for row in result:
        print(f"  - {row.statut}: {row.count}")

print("\nDone! You can now try generating EDT again.")
