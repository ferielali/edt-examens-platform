import sys
import traceback
from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models import Module, LieuExamen, Professeur, Formation, SessionGeneration, Examen, Inscription, SessionStatus, ExamStatus, InscriptionStatus
from sqlalchemy import func
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db = SessionLocal()

try:
    print("Creating session...")
    try:
        session = SessionGeneration(
            user_id=1,
            date_debut=datetime.utcnow(),
            parametres={'test': True},
            statut=SessionStatus.IN_PROGRESS
        )
        db.add(session)
        db.commit()
        print(f'Session ID: {session.id}')
    except Exception as e:
        print("Error creating session:")
        traceback.print_exc()
        db.rollback()
        sys.exit(1)

    # Get resources
    modules = db.query(Module).join(Formation).limit(1).all()
    salles = db.query(LieuExamen).filter(LieuExamen.disponible == True).limit(1).all()
    professeurs = db.query(Professeur).limit(1).all()

    if not modules:
        print("No modules found")
        sys.exit(1)

    print(f'Modules: {len(modules)}')

    # Try creating a single exam manually
    module = modules[0]
    salle = salles[0]
    prof = professeurs[0]
    slot = datetime(2026, 2, 16, 8, 0)
    
    print(f'Creating exam...')
    
    # Create exam
    examen = Examen(
        module_id=module.id,
        prof_id=prof.id,
        salle_id=salle.id,
        date_heure=slot,
        duree_minutes=120,
        statut=ExamStatus.SCHEDULED,
        session_id=session.id,
        nb_inscrits=10
    )
    db.add(examen)
    db.commit()
    print(f'Successfully created exam with ID: {examen.id}!')
    
except Exception as e:
    print(f'ERROR: {type(e).__name__}: {e}')
    with open('error_log.txt', 'w') as f:
        traceback.print_exc(file=f)
    traceback.print_exc()
finally:
    db.close()
