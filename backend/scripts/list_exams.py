# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('c:/Users/aboubakar/Desktop/Projet de fifi/backend')
os.chdir('c:/Users/aboubakar/Desktop/Projet de fifi/backend')

from dotenv import load_dotenv
load_dotenv('.env')

from sqlalchemy import create_engine, text

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

conn = engine.connect()

# Simple query for all exams
result = conn.execute(text("SELECT id, salle_id, date_heure, duree_minutes, statut FROM examens ORDER BY date_heure"))
print("All exams in database:")
for row in result:
    print(f"ID={row.id}, Room={row.salle_id}, Date={row.date_heure}, Status={row.statut}")

conn.close()
