from datetime import datetime, timedelta
from app.core.database import SessionLocal
from app.models import Module, LieuExamen, Professeur, Formation, SessionGeneration, Examen, Inscription, SessionStatus, ExamStatus, InscriptionStatus
from sqlalchemy import func
import traceback
import logging

# Enable SQLAlchemy logging to see actual errors
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

db = SessionLocal()

try:
    # Create session first
    session = SessionGeneration(
        user_id=1,
        date_debut=datetime.utcnow(),
        parametres={'test': True},
        statut=SessionStatus.IN_PROGRESS
    )
    db.add(session)
    db.commit()
    print(f'Session ID: {session.id}')

    # Get resources
    modules = db.query(Module).join(Formation).limit(3).all()
    salles = db.query(LieuExamen).filter(LieuExamen.disponible == True).limit(3).all()
    professeurs = db.query(Professeur).limit(3).all()

    print(f'Modules: {len(modules)}')
    print(f'Salles: {len(salles)}')
    print(f'Professeurs: {len(professeurs)}')

    # Generate simple time slots
    time_slots = []
    current = datetime(2026, 2, 16, 8, 0)
    for day in range(3):
        for hour in [8, 10, 14, 16]:
            time_slots.append((current + timedelta(days=day)).replace(hour=hour))
            
    print(f'Time slots: {len(time_slots)}')
    print(f'First slot: {time_slots[0]}')

    # Try creating a single exam manually
    module = modules[0]
    salle = salles[0]
    prof = professeurs[0]
    slot = time_slots[0]
    
    print(f'Creating exam for module {module.id}, salle {salle.id}, prof {prof.id}, slot {slot}')
    print(f'Module duree_examen_min: {module.duree_examen_min}, type: {type(module.duree_examen_min)}')
    
    # Get nb_inscrits
    nb_inscrits = db.query(func.count(Inscription.id)).filter(
        Inscription.module_id == module.id,
        Inscription.statut == InscriptionStatus.ACTIVE
    ).scalar() or 0
    print(f'nb_inscrits: {nb_inscrits}')
    
    duree = int(module.duree_examen_min) if module.duree_examen_min else 120
    print(f'duree: {duree}')
    
    # Create exam
    examen = Examen(
        module_id=module.id,
        prof_id=prof.id,
        salle_id=salle.id,
        date_heure=slot,
        duree_minutes=duree,
        statut=ExamStatus.SCHEDULED,
        session_id=session.id,
        nb_inscrits=nb_inscrits
    )
    db.add(examen)
    db.commit()
    print(f'Successfully created exam with ID: {examen.id}!')
    
except Exception as e:
    print(f'ERROR: {type(e).__name__}: {e}')
    traceback.print_exc()
finally:
    db.close()
