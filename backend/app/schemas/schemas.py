"""
Pydantic Schemas for API validation and serialization
"""
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class UserRoleEnum(str, Enum):
    DIRECTOR = "director"
    ADMINISTRATOR = "administrator"
    DEPARTMENT_HEAD = "department_head"
    PROFESSOR = "professor"
    STUDENT = "student"


class ExamStatusEnum(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RoomTypeEnum(str, Enum):
    AMPHI = "amphi"
    SALLE_TD = "salle_td"
    SALLE_TP = "salle_tp"
    SALLE_INFO = "salle_info"


# ============================================================================
# AUTH SCHEMAS
# ============================================================================

class Token(BaseModel):
    """JWT Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data"""
    email: Optional[str] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request"""
    email: EmailStr
    password: str = Field(min_length=6)


class RefreshRequest(BaseModel):
    """Token refresh request"""
    refresh_token: str


# ============================================================================
# USER SCHEMAS
# ============================================================================

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    nom: Optional[str] = None
    prenom: Optional[str] = None
    role: UserRoleEnum


class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(min_length=6)
    ref_id: Optional[int] = None


class UserResponse(UserBase):
    """User response schema"""
    id: int
    active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserProfile(BaseModel):
    """Current user profile"""
    id: int
    email: str
    nom: Optional[str]
    prenom: Optional[str]
    role: str
    nom_complet: str
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# DEPARTEMENT SCHEMAS
# ============================================================================

class DepartementBase(BaseModel):
    """Base departement schema"""
    nom: str = Field(max_length=100)
    code: str = Field(max_length=10)
    batiment: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None


class DepartementCreate(DepartementBase):
    """Departement creation schema"""
    pass


class DepartementResponse(DepartementBase):
    """Departement response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DepartementStats(DepartementResponse):
    """Departement with statistics"""
    nb_formations: int = 0
    nb_modules: int = 0
    nb_professeurs: int = 0
    nb_etudiants: int = 0


# ============================================================================
# FORMATION SCHEMAS
# ============================================================================

class FormationBase(BaseModel):
    """Base formation schema"""
    nom: str = Field(max_length=150)
    code: str = Field(max_length=20)
    dept_id: int
    nb_modules: int = 0
    niveau: Optional[str] = None
    type_formation: Optional[str] = None
    capacite_max: int = 100


class FormationCreate(FormationBase):
    """Formation creation schema"""
    pass


class FormationResponse(FormationBase):
    """Formation response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    departement: Optional[DepartementResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# MODULE SCHEMAS
# ============================================================================

class ModuleBase(BaseModel):
    """Base module schema"""
    nom: str = Field(max_length=150)
    code: str = Field(max_length=20)
    formation_id: int
    credits: int = Field(default=3, ge=1, le=10)
    semestre: Optional[int] = Field(default=None, ge=1, le=2)
    duree_examen_min: int = Field(default=120, ge=30, le=240)
    coefficient: float = 1.0


class ModuleCreate(ModuleBase):
    """Module creation schema"""
    pre_req_id: Optional[int] = None


class ModuleResponse(ModuleBase):
    """Module response schema"""
    id: int
    pre_req_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# LIEU EXAMEN SCHEMAS
# ============================================================================

class LieuExamenBase(BaseModel):
    """Base lieu examen schema"""
    nom: str = Field(max_length=100)
    code: str = Field(max_length=20)
    capacite: int = Field(ge=10, le=500)
    type: RoomTypeEnum = RoomTypeEnum.SALLE_TD
    batiment: str = Field(max_length=50)
    etage: int = 0
    disponible: bool = True
    equipements: dict = {}
    accessibilite_pmr: bool = False


class LieuExamenCreate(LieuExamenBase):
    """Lieu examen creation schema"""
    pass


class LieuExamenResponse(LieuExamenBase):
    """Lieu examen response schema"""
    id: int
    capacite_examen: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# PROFESSEUR SCHEMAS
# ============================================================================

class ProfesseurBase(BaseModel):
    """Base professeur schema"""
    matricule: str = Field(max_length=20)
    nom: str = Field(max_length=100)
    prenom: str = Field(max_length=100)
    dept_id: int
    specialite: Optional[str] = None
    email: EmailStr
    telephone: Optional[str] = None
    grade: Optional[str] = None
    max_surveillances: int = 3


class ProfesseurCreate(ProfesseurBase):
    """Professeur creation schema"""
    pass


class ProfesseurResponse(ProfesseurBase):
    """Professeur response schema"""
    id: int
    nom_complet: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# ETUDIANT SCHEMAS
# ============================================================================

class EtudiantBase(BaseModel):
    """Base etudiant schema"""
    matricule: str = Field(max_length=20)
    nom: str = Field(max_length=100)
    prenom: str = Field(max_length=100)
    formation_id: int
    promo: str = Field(max_length=10)
    email: EmailStr
    date_naissance: Optional[datetime] = None


class EtudiantCreate(EtudiantBase):
    """Etudiant creation schema"""
    pass


class EtudiantResponse(EtudiantBase):
    """Etudiant response schema"""
    id: int
    nom_complet: str
    created_at: datetime
    updated_at: datetime
    formation: Optional[FormationResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# INSCRIPTION SCHEMAS
# ============================================================================

class InscriptionBase(BaseModel):
    """Base inscription schema"""
    etudiant_id: int
    module_id: int
    annee_universitaire: str = "2024-2025"
    note: Optional[float] = Field(default=None, ge=0, le=20)
    statut: str = "active"


class InscriptionCreate(InscriptionBase):
    """Inscription creation schema"""
    pass


class InscriptionResponse(InscriptionBase):
    """Inscription response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# EXAMEN SCHEMAS
# ============================================================================

class ExamenBase(BaseModel):
    """Base examen schema"""
    module_id: int
    date_heure: datetime
    duree_minutes: int = Field(ge=30, le=240)


class ExamenCreate(ExamenBase):
    """Examen creation schema"""
    prof_id: Optional[int] = None
    salle_id: Optional[int] = None
    notes: Optional[str] = None


class ExamenUpdate(BaseModel):
    """Examen update schema"""
    prof_id: Optional[int] = None
    salle_id: Optional[int] = None
    date_heure: Optional[datetime] = None
    duree_minutes: Optional[int] = Field(default=None, ge=30, le=240)
    statut: Optional[ExamStatusEnum] = None
    notes: Optional[str] = None


class ExamenResponse(ExamenBase):
    """Examen response schema"""
    id: int
    prof_id: Optional[int] = None
    salle_id: Optional[int] = None
    statut: str
    session_id: Optional[int] = None
    nb_inscrits: int
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    module: Optional[ModuleResponse] = None
    professeur: Optional[ProfesseurResponse] = None
    salle: Optional[LieuExamenResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# EDT GENERATION SCHEMAS
# ============================================================================

class EDTGenerationRequest(BaseModel):
    """EDT generation request"""
    date_debut: datetime
    date_fin: datetime
    dept_ids: Optional[List[int]] = None  # None = all departments
    formation_ids: Optional[List[int]] = None
    force_regenerate: bool = False
    respect_priorites: bool = True


class EDTGenerationResponse(BaseModel):
    """EDT generation response"""
    session_id: int
    statut: str
    nb_examens_planifies: int
    nb_conflits_resolus: int
    temps_execution_ms: int
    message: str


class ConflictInfo(BaseModel):
    """Conflict information"""
    type: str
    description: str
    examens_ids: List[int]
    resolution: Optional[str] = None


# ============================================================================
# STATISTICS SCHEMAS
# ============================================================================

class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_etudiants: int
    total_professeurs: int
    total_formations: int
    total_modules: int
    total_examens_planifies: int
    total_salles: int
    taux_occupation_salles: float
    nb_conflits_actifs: int


class DepartementKPI(BaseModel):
    """Department KPIs"""
    departement_id: int
    departement_nom: str
    nb_etudiants: int
    nb_professeurs: int
    nb_examens: int
    taux_planification: float
    nb_conflits: int


# ============================================================================
# PAGINATION SCHEMAS
# ============================================================================

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
