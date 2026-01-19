"""
Dashboard and Statistics API endpoints
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user, require_department_head
from app.models import (
    User, Departement, Formation, Module, Professeur, 
    Etudiant, Inscription, Examen, LieuExamen
)
from app.schemas import (
    DashboardStats,
    DepartementKPI,
    DepartementStats,
    DepartementResponse,
    FormationResponse,
    ModuleResponse,
    ProfesseurResponse,
    EtudiantResponse,
    LieuExamenResponse,
    PaginatedResponse
)
from app.services.scheduler import get_room_occupation_stats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les statistiques globales du dashboard.
    """
    total_etudiants = db.query(func.count(Etudiant.id)).scalar() or 0
    total_professeurs = db.query(func.count(Professeur.id)).scalar() or 0
    total_formations = db.query(func.count(Formation.id)).scalar() or 0
    total_modules = db.query(func.count(Module.id)).scalar() or 0
    total_salles = db.query(func.count(LieuExamen.id)).scalar() or 0
    
    total_examens = db.query(func.count(Examen.id)).filter(
        Examen.statut.in_(['scheduled', 'confirmed'])
    ).scalar() or 0
    
    # Calcul du taux d'occupation des salles
    salles_utilisees = db.query(func.count(func.distinct(Examen.salle_id))).filter(
        Examen.statut.in_(['scheduled', 'confirmed'])
    ).scalar() or 0
    
    taux_occupation = (salles_utilisees / total_salles * 100) if total_salles > 0 else 0
    
    # Nombre de conflits actifs (simplifié)
    nb_conflits = 0  # TODO: implémenter la détection de conflits
    
    return DashboardStats(
        total_etudiants=total_etudiants,
        total_professeurs=total_professeurs,
        total_formations=total_formations,
        total_modules=total_modules,
        total_examens_planifies=total_examens,
        total_salles=total_salles,
        taux_occupation_salles=round(taux_occupation, 2),
        nb_conflits_actifs=nb_conflits
    )


@router.get("/kpi/departements", response_model=List[DepartementKPI])
async def get_departement_kpis(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_department_head)
):
    """
    Récupère les KPIs par département.
    Optimized: Uses batch queries instead of N+1 queries.
    """
    # Get all departments
    departements = db.query(Departement).all()
    
    # Pre-fetch all counts in single queries
    # Students per department
    student_counts = dict(
        db.query(Formation.dept_id, func.count(Etudiant.id))
        .join(Etudiant)
        .group_by(Formation.dept_id)
        .all()
    )
    
    # Professors per department
    prof_counts = dict(
        db.query(Professeur.dept_id, func.count(Professeur.id))
        .group_by(Professeur.dept_id)
        .all()
    )
    
    # Exams per department
    exam_counts = dict(
        db.query(Formation.dept_id, func.count(Examen.id))
        .join(Module, Module.formation_id == Formation.id)
        .join(Examen, Examen.module_id == Module.id)
        .filter(Examen.statut.in_(['scheduled', 'confirmed']))
        .group_by(Formation.dept_id)
        .all()
    )
    
    # Modules per department
    module_counts = dict(
        db.query(Formation.dept_id, func.count(Module.id))
        .join(Module)
        .group_by(Formation.dept_id)
        .all()
    )
    
    # Build KPIs from pre-fetched data
    kpis = []
    for dept in departements:
        nb_etudiants = student_counts.get(dept.id, 0)
        nb_professeurs = prof_counts.get(dept.id, 0)
        nb_examens = exam_counts.get(dept.id, 0)
        nb_modules = module_counts.get(dept.id, 0)
        
        taux = (nb_examens / nb_modules * 100) if nb_modules > 0 else 0
        
        kpis.append(DepartementKPI(
            departement_id=dept.id,
            departement_nom=dept.nom,
            nb_etudiants=nb_etudiants,
            nb_professeurs=nb_professeurs,
            nb_examens=nb_examens,
            taux_planification=round(taux, 2),
            nb_conflits=0
        ))
    
    return kpis


@router.get("/salles/occupation")
async def get_occupation_salles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les statistiques d'occupation des salles.
    """
    return get_room_occupation_stats(db)


# ============================================================================
# CRUD ENDPOINTS POUR LES ENTITÉS
# ============================================================================

# Départements
@router.get("/departements", response_model=List[DepartementStats])
async def list_departements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste tous les départements avec statistiques (optimized)"""
    departements = db.query(Departement).all()
    
    # Pre-fetch all counts in batch queries
    formation_counts = dict(
        db.query(Formation.dept_id, func.count(Formation.id))
        .group_by(Formation.dept_id)
        .all()
    )
    
    module_counts = dict(
        db.query(Formation.dept_id, func.count(Module.id))
        .join(Module)
        .group_by(Formation.dept_id)
        .all()
    )
    
    prof_counts = dict(
        db.query(Professeur.dept_id, func.count(Professeur.id))
        .group_by(Professeur.dept_id)
        .all()
    )
    
    student_counts = dict(
        db.query(Formation.dept_id, func.count(Etudiant.id))
        .join(Etudiant)
        .group_by(Formation.dept_id)
        .all()
    )
    
    result = []
    for dept in departements:
        result.append(DepartementStats(
            id=dept.id,
            nom=dept.nom,
            code=dept.code,
            batiment=dept.batiment,
            telephone=dept.telephone,
            email=dept.email,
            created_at=dept.created_at,
            updated_at=dept.updated_at,
            nb_formations=formation_counts.get(dept.id, 0),
            nb_modules=module_counts.get(dept.id, 0),
            nb_professeurs=prof_counts.get(dept.id, 0),
            nb_etudiants=student_counts.get(dept.id, 0)
        ))
    
    return result


# Formations
@router.get("/formations", response_model=PaginatedResponse)
async def list_formations(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    dept_id: Optional[int] = None,
    niveau: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les formations avec pagination"""
    query = db.query(Formation)
    
    if dept_id:
        query = query.filter(Formation.dept_id == dept_id)
    if niveau:
        query = query.filter(Formation.niveau == niveau)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=[FormationResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


# Modules
@router.get("/modules", response_model=PaginatedResponse)
async def list_modules(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    formation_id: Optional[int] = None,
    semestre: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les modules avec pagination"""
    query = db.query(Module)
    
    if formation_id:
        query = query.filter(Module.formation_id == formation_id)
    if semestre:
        query = query.filter(Module.semestre == semestre)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=[ModuleResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


# Professeurs
@router.get("/professeurs", response_model=PaginatedResponse)
async def list_professeurs(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    dept_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les professeurs avec pagination"""
    query = db.query(Professeur)
    
    if dept_id:
        query = query.filter(Professeur.dept_id == dept_id)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=[ProfesseurResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


# Étudiants
@router.get("/etudiants", response_model=PaginatedResponse)
async def list_etudiants(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    formation_id: Optional[int] = None,
    promo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_department_head)
):
    """Liste les étudiants avec pagination"""
    query = db.query(Etudiant)
    
    if formation_id:
        query = query.filter(Etudiant.formation_id == formation_id)
    if promo:
        query = query.filter(Etudiant.promo == promo)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=[EtudiantResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


# Salles
@router.get("/salles", response_model=List[LieuExamenResponse])
async def list_salles(
    type: Optional[str] = None,
    batiment: Optional[str] = None,
    disponible: Optional[bool] = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste les salles d'examen"""
    query = db.query(LieuExamen)
    
    if type:
        query = query.filter(LieuExamen.type == type)
    if batiment:
        query = query.filter(LieuExamen.batiment == batiment)
    if disponible is not None:
        query = query.filter(LieuExamen.disponible == disponible)
    
    salles = query.all()
    
    # Ajouter capacite_examen manuellement
    result = []
    for salle in salles:
        salle_dict = {
            "id": salle.id,
            "nom": salle.nom,
            "code": salle.code,
            "capacite": salle.capacite,
            "capacite_examen": salle.capacite // 2,
            "type": salle.type,
            "batiment": salle.batiment,
            "etage": salle.etage,
            "disponible": salle.disponible,
            "equipements": salle.equipements or {},
            "accessibilite_pmr": salle.accessibilite_pmr,
            "created_at": salle.created_at,
            "updated_at": salle.updated_at
        }
        result.append(LieuExamenResponse.model_validate(salle_dict))
    
    return result
