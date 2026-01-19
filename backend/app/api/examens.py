"""
Exam and EDT API endpoints
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.core.security import get_current_user, require_admin, require_department_head
from app.models import Examen, Module, User, Formation, Departement
from app.schemas import (
    ExamenCreate,
    ExamenUpdate,
    ExamenResponse,
    EDTGenerationRequest,
    EDTGenerationResponse,
    ConflictInfo,
    PaginatedResponse
)
from app.services.scheduler import ExamScheduler, detect_conflicts

router = APIRouter(prefix="/examens", tags=["Examens"])


@router.get("/", response_model=PaginatedResponse)
async def list_examens(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    dept_id: Optional[int] = None,
    formation_id: Optional[int] = None,
    statut: Optional[str] = None,
    date_debut: Optional[datetime] = None,
    date_fin: Optional[datetime] = None,
    search: Optional[str] = None,
    sort_order: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Liste des examens avec filtres et pagination.
    """
    query = db.query(Examen).join(Module).join(Formation)
    
    # Appliquer les filtres
    if dept_id:
        query = query.filter(Formation.dept_id == dept_id)
    if formation_id:
        query = query.filter(Module.formation_id == formation_id)
    if statut:
        query = query.filter(Examen.statut == statut)
    if date_debut:
        query = query.filter(Examen.date_heure >= date_debut)
    if date_fin:
        query = query.filter(Examen.date_heure <= date_fin)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Module.nom.ilike(search_term)) | (Module.code.ilike(search_term))
        )
    
    # Filtrer par rôle
    if current_user.role == "department_head" and current_user.ref_id:
        query = query.filter(Formation.dept_id == current_user.ref_id)
    elif current_user.role == "professor" and current_user.ref_id:
        query = query.filter(Examen.prof_id == current_user.ref_id)
    elif current_user.role == "student" and current_user.ref_id:
        # Les étudiants voient seulement leurs examens
        from app.models import Inscription, Etudiant
        student = db.query(Etudiant).filter(Etudiant.id == current_user.ref_id).first()
        if student:
            inscribed_modules = db.query(Inscription.module_id).filter(
                Inscription.etudiant_id == student.id,
                Inscription.statut == 'active'
            ).subquery()
            query = query.filter(Examen.module_id.in_(inscribed_modules))
    
    # Pagination avec tri
    total = query.count()
    if sort_order == 'desc':
        items = query.order_by(Examen.date_heure.desc()).offset((page - 1) * size).limit(size).all()
    else:
        items = query.order_by(Examen.date_heure).offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=[ExamenResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.get("/{examen_id}", response_model=ExamenResponse)
async def get_examen(
    examen_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère un examen par son ID.
    """
    examen = db.query(Examen).filter(Examen.id == examen_id).first()
    
    if not examen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examen non trouvé"
        )
    
    return examen


@router.post("/", response_model=ExamenResponse, status_code=status.HTTP_201_CREATED)
async def create_examen(
    examen_data: ExamenCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Crée un nouvel examen (admin uniquement).
    """
    # Vérifier que le module existe
    module = db.query(Module).filter(Module.id == examen_data.module_id).first()
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module non trouvé"
        )
    
    examen = Examen(
        module_id=examen_data.module_id,
        prof_id=examen_data.prof_id,
        salle_id=examen_data.salle_id,
        date_heure=examen_data.date_heure,
        duree_minutes=examen_data.duree_minutes,
        notes=examen_data.notes,
        statut="draft"
    )
    
    db.add(examen)
    db.commit()
    db.refresh(examen)
    
    return examen


@router.put("/{examen_id}", response_model=ExamenResponse)
async def update_examen(
    examen_id: int,
    examen_data: ExamenUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_department_head)
):
    """
    Met à jour un examen.
    """
    examen = db.query(Examen).filter(Examen.id == examen_id).first()
    
    if not examen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examen non trouvé"
        )
    
    # Mettre à jour les champs
    update_data = examen_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(examen, key, value.value if hasattr(value, 'value') else value)
    
    db.commit()
    db.refresh(examen)
    
    return examen


@router.delete("/{examen_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_examen(
    examen_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Supprime un examen (admin uniquement).
    """
    examen = db.query(Examen).filter(Examen.id == examen_id).first()
    
    if not examen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examen non trouvé"
        )
    
    db.delete(examen)
    db.commit()


@router.post("/generate", response_model=EDTGenerationResponse)
async def generate_edt(
    request: EDTGenerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Génère automatiquement un EDT optimisé.
    
    Utilise l'algorithme OR-Tools pour résoudre les contraintes:
    - Maximum 1 examen par jour par étudiant
    - Maximum 3 examens par jour par professeur
    - Respect des capacités des salles
    - Pas de chevauchement horaire
    """
    try:
        scheduler = ExamScheduler(db)
        result = scheduler.generate_schedule(
            date_debut=request.date_debut,
            date_fin=request.date_fin,
            dept_ids=request.dept_ids,
            formation_ids=request.formation_ids,
            user_id=current_user.id
        )
        
        return EDTGenerationResponse(
            session_id=result["session_id"],
            statut=result["statut"],
            nb_examens_planifies=result["nb_examens_planifies"],
            nb_conflits_resolus=result["nb_conflits_resolus"],
            temps_execution_ms=result["temps_execution_ms"],
            message=result["message"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la génération de l'EDT: {str(e)}"
        )


@router.get("/conflicts/detect", response_model=List[ConflictInfo])
async def detect_exam_conflicts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_department_head)
):
    """
    Détecte les conflits dans l'EDT actuel.
    """
    conflicts = detect_conflicts(db)
    
    return [ConflictInfo(
        type=c["type"],
        description=c["description"],
        examens_ids=c["examens_ids"],
        resolution=None
    ) for c in conflicts]


@router.post("/{examen_id}/confirm")
async def confirm_examen(
    examen_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_department_head)
):
    """
    Confirme un examen planifié.
    """
    examen = db.query(Examen).filter(Examen.id == examen_id).first()
    
    if not examen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examen non trouvé"
        )
    
    if examen.statut not in ["draft", "scheduled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seuls les examens en brouillon ou planifiés peuvent être confirmés"
        )
    
    examen.statut = "confirmed"
    db.commit()
    
    return {"message": "Examen confirmé avec succès"}


@router.post("/{examen_id}/cancel")
async def cancel_examen(
    examen_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Annule un examen.
    """
    examen = db.query(Examen).filter(Examen.id == examen_id).first()
    
    if not examen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Examen non trouvé"
        )
    
    examen.statut = "cancelled"
    db.commit()
    
    return {"message": "Examen annulé avec succès"}
