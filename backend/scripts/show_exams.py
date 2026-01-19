# -*- coding: utf-8 -*-
"""Show all exams and their room/time assignments"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

with engine.connect() as conn:
    print("=" * 80)
    print("ALL NON-CANCELLED EXAMS (showing room conflicts)")
    print("=" * 80)
    
    result = conn.execute(text("""
        SELECT e.id, e.module_id, m.nom as module_nom, 
               e.salle_id, l.nom as salle_nom,
               e.date_heure, e.duree_minutes, e.statut
        FROM examens e
        LEFT JOIN modules m ON m.id = e.module_id
        LEFT JOIN lieux_examen l ON l.id = e.salle_id
        WHERE e.statut NOT IN ('cancelled')
        ORDER BY e.date_heure, e.salle_id
    """))
    
    rows = result.fetchall()
    print(f"\nFound {len(rows)} exams:\n")
    print(f"{'ID':<5} {'Room':<15} {'Date/Time':<20} {'Duration':<10} {'Status':<12} {'Module'}")
    print("-" * 80)
    
    for row in rows:
        date_str = row.date_heure.strftime('%Y-%m-%d %H:%M') if row.date_heure else 'N/A'
        salle = row.salle_nom if row.salle_nom else 'None'
        module = row.module_nom[:30] if row.module_nom else 'N/A'
        print(f"{row.id:<5} {salle:<15} {date_str:<20} {row.duree_minutes or 0:<10} {row.statut:<12} {module}")
    
    # Check what date range the next generation would use
    print("\n" + "=" * 80)
    print("DEFAULT GENERATION PERIOD: 16/02/2026 - 02/03/2026")
    print("First slots would be: 2026-02-16 08:00, 10:00, 14:00, 16:00")
    print("=" * 80)
