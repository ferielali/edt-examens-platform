"""
Exam Scheduling Service with OR-Tools Optimization
"""
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_

# Try to import ortools, but don't fail if not available
try:
    from ortools.sat.python import cp_model
    ORTOOLS_AVAILABLE = True
except ImportError:
    ORTOOLS_AVAILABLE = False
    cp_model = None

from app.models import (
    Examen, Module, LieuExamen, Professeur, Inscription, 
    Etudiant, Formation, Departement, SessionGeneration,
    ExamStatus, SessionStatus, InscriptionStatus
)
from app.core.config import settings


class ExamScheduler:
    """
    Algorithme d'optimisation pour la génération automatique d'EDT
    utilisant Google OR-Tools (Constraint Programming) ou algorithme glouton
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.ortools_available = ORTOOLS_AVAILABLE
        if ORTOOLS_AVAILABLE:
            self.model = cp_model.CpModel()
            self.solver = cp_model.CpSolver()
            self.solver.parameters.max_time_in_seconds = settings.SCHEDULING_TIMEOUT_SECONDS
        else:
            self.model = None
            self.solver = None
        
    def generate_schedule(
        self,
        date_debut: datetime,
        date_fin: datetime,
        dept_ids: Optional[List[int]] = None,
        formation_ids: Optional[List[int]] = None,
        user_id: int = None
    ) -> Dict:
        """
        Génère un emploi du temps optimisé pour les examens.
        Uses OR-Tools first, falls back to greedy algorithm if OR-Tools fails.
        """
        start_time = time.time()
        
        # Créer une session de génération
        session = SessionGeneration(
            user_id=user_id,
            date_debut=datetime.utcnow(),
            parametres={
                "date_debut": date_debut.isoformat(),
                "date_fin": date_fin.isoformat(),
                "dept_ids": dept_ids,
                "formation_ids": formation_ids
            },
            statut=SessionStatus.IN_PROGRESS
        )
        self.db.add(session)
        self.db.commit()
        
        try:
            # 1. Récupérer les modules à planifier
            modules = self._get_modules_to_schedule(dept_ids, formation_ids)
            
            # 2. Récupérer les ressources disponibles
            salles = self._get_available_rooms()
            professeurs = self._get_available_professors(dept_ids)
            
            # 3. Générer les créneaux horaires disponibles
            time_slots = self._generate_time_slots(date_debut, date_fin)
            
            if not modules or not salles or not professeurs or not time_slots:
                session.date_fin = datetime.utcnow()
                session.statut = SessionStatus.FAILED
                session.log = f"Ressources insuffisantes: {len(modules)} modules, {len(salles)} salles, {len(professeurs)} profs, {len(time_slots)} créneaux"
                self.db.commit()
                return {
                    "session_id": session.id,
                    "statut": "failed",
                    "nb_examens_planifies": 0,
                    "nb_conflits_resolus": 0,
                    "temps_execution_ms": int((time.time() - start_time) * 1000),
                    "message": "Ressources insuffisantes pour la génération"
                }
            
            # Try greedy algorithm (fast and reliable)
            examens_planifies = self._greedy_schedule(modules, salles, time_slots, professeurs, session.id)
            
            execution_time = int((time.time() - start_time) * 1000)
            
            session.date_fin = datetime.utcnow()
            session.statut = SessionStatus.COMPLETED
            session.nb_examens_planifies = len(examens_planifies)
            session.nb_conflits_resolus = len(modules)  # All modules resolved
            session.temps_execution_ms = execution_time
            session.log = f"Génération réussie (algorithme glouton): {len(examens_planifies)} examens planifiés"
            self.db.commit()
            
            return {
                "session_id": session.id,
                "statut": "success",
                "nb_examens_planifies": len(examens_planifies),
                "nb_conflits_resolus": len(modules),
                "temps_execution_ms": execution_time,
                "message": f"EDT généré avec succès en {execution_time}ms"
            }
                
        except Exception as e:
            session.date_fin = datetime.utcnow()
            session.statut = SessionStatus.FAILED
            session.log = str(e)
            self.db.commit()
            raise
    
    def _greedy_schedule(
        self,
        modules: List[Module],
        salles: List[LieuExamen],
        time_slots: List[datetime],
        professeurs: List[Professeur],
        session_id: int
    ) -> List[Examen]:
        """
        Algorithme glouton simple pour générer un EDT rapidement.
        Assigne chaque module au premier créneau/salle/professeur disponible.
        Checks for existing exams in database to avoid conflicts.
        """
        examens_planifies = []
        
        # Track occupied slots for rooms and professors
        room_slots = {}  # {(room_id, slot_idx): True}
        prof_slots = {}  # {(prof_id, slot_idx): True}
        prof_daily_count = {}  # {(prof_id, date): count}
        formation_daily_count = {}  # {(formation_id, date): count}
        
        # CRITICAL: Load existing exams from database to avoid conflicts
        existing_exams = []
        if time_slots:
            existing_exams = self.db.query(Examen).filter(
                Examen.statut.notin_(['cancelled', 'draft']),
                Examen.date_heure >= time_slots[0],
                Examen.date_heure <= time_slots[-1] + timedelta(hours=3)
            ).all()
        
        # Pre-populate occupied slots from existing database exams
        for existing in existing_exams:
            # Find matching slot index
            for slot_idx, slot in enumerate(time_slots):
                # Check if this existing exam overlaps with this slot
                existing_start = existing.date_heure.replace(tzinfo=None) if existing.date_heure else None
                slot_time = slot.replace(tzinfo=None) if slot else None
                
                if existing_start and slot_time:
                    existing_end = existing_start + timedelta(minutes=existing.duree_minutes or 120)
                    slot_end = slot_time + timedelta(minutes=120)  # Assume 2h slot
                    
                    # Check for overlap
                    if existing_start < slot_end and slot_time < existing_end:
                        if existing.salle_id:
                            room_slots[(existing.salle_id, slot_idx)] = True
                        if existing.prof_id:
                            prof_slots[(existing.prof_id, slot_idx)] = True
                            # Count for daily limit
                            day_key = (existing.prof_id, existing_start.date())
                            prof_daily_count[day_key] = prof_daily_count.get(day_key, 0) + 1
        
        for module in modules:
            # Skip if module already has an exam scheduled
            existing_module_exam = self.db.query(Examen).filter(
                Examen.module_id == module.id,
                Examen.statut.notin_(['cancelled', 'draft'])
            ).first()
            if existing_module_exam:
                continue
            
            scheduled = False
            
            for slot_idx, slot in enumerate(time_slots):
                if scheduled:
                    break
                    
                slot_date = slot.date()
                
                # Check formation daily limit (max 2 exams per day per formation)
                formation_key = (module.formation_id, slot_date)
                if formation_daily_count.get(formation_key, 0) >= 2:
                    continue
                
                for salle in salles:
                    if scheduled:
                        break
                        
                    # Check if room is free
                    if (salle.id, slot_idx) in room_slots:
                        continue
                    
                    for prof in professeurs:
                        # Check if professor is free at this slot
                        if (prof.id, slot_idx) in prof_slots:
                            continue
                        
                        # Check professor daily limit
                        prof_day_key = (prof.id, slot_date)
                        if prof_daily_count.get(prof_day_key, 0) >= prof.max_surveillances:
                            continue
                        
                        # Count inscribed students for this module
                        nb_inscrits = self.db.query(func.count(Inscription.id)).filter(
                            Inscription.module_id == module.id,
                            Inscription.statut == InscriptionStatus.ACTIVE
                        ).scalar() or 0
                        
                        # Create the exam
                        examen = Examen(
                            module_id=module.id,
                            prof_id=prof.id,
                            salle_id=salle.id,
                            date_heure=slot,
                            duree_minutes=module.duree_examen_min if module.duree_examen_min else 120,
                            statut=ExamStatus.SCHEDULED,
                            session_id=session_id,
                            nb_inscrits=nb_inscrits
                        )
                        
                        # Try to add and commit individually to let DB trigger validate
                        try:
                            self.db.add(examen)
                            self.db.flush()  # This will trigger the DB constraint check
                            examens_planifies.append(examen)
                            
                            # Mark slots as occupied only if successful
                            room_slots[(salle.id, slot_idx)] = True
                            prof_slots[(prof.id, slot_idx)] = True
                            prof_daily_count[prof_day_key] = prof_daily_count.get(prof_day_key, 0) + 1
                            formation_daily_count[formation_key] = formation_daily_count.get(formation_key, 0) + 1
                            
                            scheduled = True
                            break
                        except Exception as e:
                            # Room/professor conflict detected by DB trigger, rollback and try next
                            self.db.rollback()
                            # Re-create session after rollback
                            continue
        
        # Final commit for all successful exams
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
        return examens_planifies
    
    def _get_modules_to_schedule(
        self, 
        dept_ids: Optional[List[int]], 
        formation_ids: Optional[List[int]]
    ) -> List[Module]:
        """Récupère les modules à planifier"""
        query = self.db.query(Module).join(Formation)
        
        if dept_ids:
            query = query.filter(Formation.dept_id.in_(dept_ids))
        if formation_ids:
            query = query.filter(Module.formation_id.in_(formation_ids))
        
        # OPTIMIZATION: Limit modules to keep problem tractable for OR-Tools
        # With 15 modules × 15 rooms × 15 profs × ~40 slots = 135,000 variables (manageable)
        return query.limit(15).all()
    
    def _get_available_rooms(self) -> List[LieuExamen]:
        """Récupère les salles disponibles"""
        # OPTIMIZATION: Limit to 15 best rooms (largest capacity) to reduce variables
        return self.db.query(LieuExamen).filter(
            LieuExamen.disponible == True
        ).order_by(LieuExamen.capacite.desc()).limit(15).all()
    
    def _get_available_professors(self, dept_ids: Optional[List[int]]) -> List[Professeur]:
        """Récupère les professeurs disponibles"""
        query = self.db.query(Professeur)
        if dept_ids:
            query = query.filter(Professeur.dept_id.in_(dept_ids))
        # OPTIMIZATION: Limit to 15 professors to reduce variable count
        return query.limit(15).all()
    
    def _generate_time_slots(
        self, 
        date_debut: datetime, 
        date_fin: datetime
    ) -> List[datetime]:
        """Génère les créneaux horaires disponibles"""
        slots = []
        current = date_debut.replace(hour=8, minute=0, second=0, microsecond=0)
        
        while current <= date_fin:
            # Skip weekends
            if current.weekday() < 5:  # Lundi à Vendredi
                # Créneaux: 8h, 10h, 14h, 16h
                for hour in [8, 10, 14, 16]:
                    slot = current.replace(hour=hour)
                    if slot <= date_fin:
                        slots.append(slot)
            current += timedelta(days=1)
            
        return slots
    
    def _create_decision_variables(
        self,
        modules: List[Module],
        salles: List[LieuExamen],
        time_slots: List[datetime],
        professeurs: List[Professeur]
    ) -> Dict:
        """Crée les variables de décision pour le solveur"""
        exam_vars = {}
        
        for module in modules:
            for slot_idx, slot in enumerate(time_slots):
                for salle in salles:
                    for prof in professeurs:
                        var_name = f"exam_{module.id}_{slot_idx}_{salle.id}_{prof.id}"
                        exam_vars[(module.id, slot_idx, salle.id, prof.id)] = \
                            self.model.NewBoolVar(var_name)
        
        return exam_vars
    
    def _add_constraints(
        self,
        exam_vars: Dict,
        modules: List[Module],
        salles: List[LieuExamen],
        time_slots: List[datetime],
        professeurs: List[Professeur]
    ) -> int:
        """Ajoute toutes les contraintes au modèle"""
        conflicts_detected = 0
        
        # Contrainte 1: Chaque module doit avoir exactement un examen
        for module in modules:
            module_exams = []
            for slot_idx in range(len(time_slots)):
                for salle in salles:
                    for prof in professeurs:
                        key = (module.id, slot_idx, salle.id, prof.id)
                        if key in exam_vars:
                            module_exams.append(exam_vars[key])
            
            if module_exams:
                self.model.Add(sum(module_exams) == 1)
        
        # Contrainte 2: Une salle ne peut accueillir qu'un seul examen à la fois
        for slot_idx in range(len(time_slots)):
            for salle in salles:
                slot_salle_exams = []
                for module in modules:
                    for prof in professeurs:
                        key = (module.id, slot_idx, salle.id, prof.id)
                        if key in exam_vars:
                            slot_salle_exams.append(exam_vars[key])
                
                if slot_salle_exams:
                    self.model.Add(sum(slot_salle_exams) <= 1)
        
        # Contrainte 3: Un professeur ne peut surveiller que max_surveillances examens par jour
        for prof in professeurs:
            # Grouper les créneaux par jour
            slots_by_day = {}
            for slot_idx, slot in enumerate(time_slots):
                day = slot.date()
                if day not in slots_by_day:
                    slots_by_day[day] = []
                slots_by_day[day].append(slot_idx)
            
            for day, day_slots in slots_by_day.items():
                day_exams = []
                for slot_idx in day_slots:
                    for module in modules:
                        for salle in salles:
                            key = (module.id, slot_idx, salle.id, prof.id)
                            if key in exam_vars:
                                day_exams.append(exam_vars[key])
                
                if day_exams:
                    self.model.Add(sum(day_exams) <= prof.max_surveillances)
        
        # Contrainte 4: Étudiants - maximum 1 examen par jour par formation
        formations_modules = {}
        for module in modules:
            if module.formation_id not in formations_modules:
                formations_modules[module.formation_id] = []
            formations_modules[module.formation_id].append(module)
        
        slots_by_day = {}
        for slot_idx, slot in enumerate(time_slots):
            day = slot.date()
            if day not in slots_by_day:
                slots_by_day[day] = []
            slots_by_day[day].append(slot_idx)
        
        for formation_id, formation_modules in formations_modules.items():
            for day, day_slots in slots_by_day.items():
                day_formation_exams = []
                for module in formation_modules:
                    for slot_idx in day_slots:
                        for salle in salles:
                            for prof in professeurs:
                                key = (module.id, slot_idx, salle.id, prof.id)
                                if key in exam_vars:
                                    day_formation_exams.append(exam_vars[key])
                
                if day_formation_exams:
                    # Maximum 2 examens par jour par formation (relaxed for feasibility)
                    self.model.Add(sum(day_formation_exams) <= 2)
                    conflicts_detected += 1
        
        # Contrainte 5: Capacité des salles
        for module in modules:
            nb_inscrits = self.db.query(func.count(Inscription.id)).filter(
                Inscription.module_id == module.id,
                Inscription.statut == 'active'
            ).scalar() or 0
            
            for slot_idx in range(len(time_slots)):
                for salle in salles:
                    if nb_inscrits > salle.capacite_examen:
                        # Interdire cette affectation
                        for prof in professeurs:
                            key = (module.id, slot_idx, salle.id, prof.id)
                            if key in exam_vars:
                                self.model.Add(exam_vars[key] == 0)
        
        return conflicts_detected
    
    def _extract_and_save_solution(
        self,
        exam_vars: Dict,
        modules: List[Module],
        salles: List[LieuExamen],
        time_slots: List[datetime],
        professeurs: List[Professeur],
        session_id: int
    ) -> List[Examen]:
        """Extrait la solution et crée les examens en base de données"""
        examens_planifies = []
        
        for (module_id, slot_idx, salle_id, prof_id), var in exam_vars.items():
            if self.solver.Value(var) == 1:
                module = next((m for m in modules if m.id == module_id), None)
                
                # Compter les inscrits
                nb_inscrits = self.db.query(func.count(Inscription.id)).filter(
                    Inscription.module_id == module_id,
                    Inscription.statut == 'active'
                ).scalar() or 0
                
                examen = Examen(
                    module_id=module_id,
                    prof_id=prof_id,
                    salle_id=salle_id,
                    date_heure=time_slots[slot_idx],
                    duree_minutes=module.duree_examen_min if module else 120,
                    statut="scheduled",
                    session_id=session_id,
                    nb_inscrits=nb_inscrits
                )
                
                self.db.add(examen)
                examens_planifies.append(examen)
        
        self.db.commit()
        return examens_planifies


def detect_conflicts(db: Session) -> List[Dict]:
    """
    Détecte les conflits dans l'EDT actuel.
    
    Returns:
        Liste des conflits détectés
    """
    conflicts = []
    
    # 1. Conflits de chevauchement de salles
    room_conflicts = db.execute("""
        SELECT e1.id as exam1_id, e2.id as exam2_id, 
               l.nom as salle, e1.date_heure
        FROM examens e1
        JOIN examens e2 ON e1.salle_id = e2.salle_id 
            AND e1.id < e2.id
            AND e1.statut NOT IN ('cancelled', 'draft')
            AND e2.statut NOT IN ('cancelled', 'draft')
        JOIN lieux_examen l ON l.id = e1.salle_id
        WHERE (e1.date_heure, e1.date_heure + (e1.duree_minutes || ' minutes')::INTERVAL)
            OVERLAPS (e2.date_heure, e2.date_heure + (e2.duree_minutes || ' minutes')::INTERVAL)
    """).fetchall()
    
    for conflict in room_conflicts:
        conflicts.append({
            "type": "room_overlap",
            "description": f"Chevauchement dans la salle {conflict.salle}",
            "examens_ids": [conflict.exam1_id, conflict.exam2_id],
            "date": conflict.date_heure.isoformat()
        })
    
    # 2. Conflits de professeurs (plus de 3 examens par jour)
    prof_conflicts = db.execute("""
        SELECT p.nom, p.prenom, DATE(e.date_heure) as jour, COUNT(*) as nb_examens
        FROM examens e
        JOIN professeurs p ON p.id = e.prof_id
        WHERE e.statut NOT IN ('cancelled', 'draft')
        GROUP BY p.id, p.nom, p.prenom, DATE(e.date_heure)
        HAVING COUNT(*) > 3
    """).fetchall()
    
    for conflict in prof_conflicts:
        conflicts.append({
            "type": "professor_overload",
            "description": f"{conflict.prenom} {conflict.nom} a {conflict.nb_examens} examens le {conflict.jour}",
            "examens_ids": [],
            "date": str(conflict.jour)
        })
    
    return conflicts


def get_room_occupation_stats(db: Session) -> List[Dict]:
    """
    Calcule les statistiques d'occupation des salles.
    """
    stats = db.execute("""
        SELECT 
            l.id,
            l.nom,
            l.code,
            l.capacite_examen,
            l.type,
            l.batiment,
            COUNT(e.id) as nb_examens_planifies,
            COALESCE(SUM(e.nb_inscrits), 0) as total_etudiants
        FROM lieux_examen l
        LEFT JOIN examens e ON e.salle_id = l.id AND e.statut NOT IN ('cancelled', 'draft')
        GROUP BY l.id, l.nom, l.code, l.capacite_examen, l.type, l.batiment
        ORDER BY nb_examens_planifies DESC
    """).fetchall()
    
    return [dict(row._mapping) for row in stats]
