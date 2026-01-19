# -*- coding: utf-8 -*-
"""Test EDT Generation"""
import os
import sys
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Examen, Module, LieuExamen, Professeur, SessionGeneration

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
db = Session()

print("=" * 60)
print("EDT GENERATION DEBUG")
print("=" * 60)

# Check existing exams
existing_exams = db.query(Examen).filter(
    Examen.statut.notin_(['cancelled', 'draft'])
).count()
print(f"\n1. Existing non-cancelled/draft exams: {existing_exams}")

# Check modules
modules = db.query(Module).limit(5).all()
print(f"\n2. Modules to schedule: {len(modules)}")
for m in modules:
    has_exam = db.query(Examen).filter(
        Examen.module_id == m.id,
        Examen.statut.notin_(['cancelled', 'draft'])
    ).first()
    print(f"   - Module {m.id}: {m.nom[:30]}... -> {'HAS EXAM' if has_exam else 'No exam'}")

# Check available rooms
rooms = db.query(LieuExamen).filter(LieuExamen.disponible == True).limit(5).all()
print(f"\n3. Available rooms: {len(rooms)}")
for r in rooms:
    print(f"   - Room {r.id}: {r.nom} (capacity: {r.capacite_examen})")

# Check professors
profs = db.query(Professeur).limit(5).all()
print(f"\n4. Available professors: {len(profs)}")
for p in profs:
    print(f"   - Prof {p.id}: {p.prenom} {p.nom}")

# Check for room conflicts in specific date range
test_date = datetime(2026, 2, 16, 8, 0)
print(f"\n5. Checking rooms occupied on {test_date}:")
occupied = db.execute(text("""
    SELECT e.id, e.salle_id, l.nom as salle_nom, e.date_heure, e.duree_minutes, e.statut
    FROM examens e
    JOIN lieux_examen l ON l.id = e.salle_id
    WHERE DATE(e.date_heure) = '2026-02-16'
    AND e.statut NOT IN ('cancelled', 'draft')
    ORDER BY e.date_heure
""")).fetchall()

if occupied:
    for o in occupied:
        print(f"   - Exam {o.id}: Room '{o.salle_nom}' at {o.date_heure} ({o.duree_minutes}min) - {o.statut}")
else:
    print("   No exams found on that date")

print("\n" + "=" * 60)
print("RECOMMENDATION:")
if existing_exams > 0:
    print("There are existing exams. To test fresh generation, you can:")
    print("1. Delete existing scheduled exams first")
    print("2. Or change the date range to a future period without exams")
print("=" * 60)

db.close()
