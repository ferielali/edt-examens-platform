"""
SQLAlchemy Models for the Exam Scheduler Platform
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, 
    Text, Numeric, Enum, JSON, CheckConstraint, UniqueConstraint,
    Computed
)
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


# ============================================================================
# ENUMS
# ============================================================================

class UserRole(str, enum.Enum):
    DIRECTOR = "director"
    ADMINISTRATOR = "administrator"
    DEPARTMENT_HEAD = "department_head"
    PROFESSOR = "professor"
    STUDENT = "student"


class ExamStatus(str, enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class InscriptionStatus(enum.Enum):
    ACTIVE = "active"
    WITHDRAWN = "withdrawn"
    COMPLETED = "completed"


class RoomType(enum.Enum):
    AMPHI = "amphi"
    SALLE_TD = "salle_td"
    SALLE_TP = "salle_tp"
    SALLE_INFO = "salle_info"


class SessionStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================================================
# MODELS
# ============================================================================

class Departement(Base):
    """Départements universitaires"""
    __tablename__ = "departements"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    code = Column(String(10), unique=True, nullable=False, index=True)
    batiment = Column(String(50))
    telephone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    formations = relationship("Formation", back_populates="departement")
    professeurs = relationship("Professeur", back_populates="departement")


class Formation(Base):
    """Formations académiques"""
    __tablename__ = "formations"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    dept_id = Column(Integer, ForeignKey("departements.id", ondelete="RESTRICT"), nullable=False)
    nb_modules = Column(Integer, default=0)
    niveau = Column(String(20))
    type_formation = Column(String(50))
    capacite_max = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    departement = relationship("Departement", back_populates="formations")
    modules = relationship("Module", back_populates="formation")
    etudiants = relationship("Etudiant", back_populates="formation")
    
    __table_args__ = (
        CheckConstraint("niveau IN ('L1', 'L2', 'L3', 'M1', 'M2', 'D')"),
        CheckConstraint("type_formation IN ('licence', 'master', 'doctorat')"),
    )


class Module(Base):
    """Modules/Matières"""
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(150), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    formation_id = Column(Integer, ForeignKey("formations.id", ondelete="CASCADE"), nullable=False)
    credits = Column(Integer, default=3)
    semestre = Column(Integer)
    pre_req_id = Column(Integer, ForeignKey("modules.id", ondelete="SET NULL"))
    duree_examen_min = Column(Integer, default=120)
    coefficient = Column(Numeric(3, 1), default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    formation = relationship("Formation", back_populates="modules")
    inscriptions = relationship("Inscription", back_populates="module")
    examens = relationship("Examen", back_populates="module")
    prerequis = relationship("Module", remote_side=[id])
    
    __table_args__ = (
        CheckConstraint("credits >= 1 AND credits <= 10"),
        CheckConstraint("semestre >= 1 AND semestre <= 2"),
        CheckConstraint("duree_examen_min >= 30 AND duree_examen_min <= 240"),
    )


class LieuExamen(Base):
    """Salles d'examen"""
    __tablename__ = "lieux_examen"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    capacite = Column(Integer, nullable=False)
    type = Column(Enum(RoomType, name="room_type", values_callable=lambda x: [e.value for e in x]), default=RoomType.SALLE_TD)
    batiment = Column(String(50), nullable=False)
    etage = Column(Integer, default=0)
    disponible = Column(Boolean, default=True)
    equipements = Column(JSON, default={})
    accessibilite_pmr = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    examens = relationship("Examen", back_populates="salle")
    
    @property
    def capacite_examen(self) -> int:
        """Capacité pendant les examens (divisée par 2)"""
        return self.capacite // 2
    
    __table_args__ = (
        CheckConstraint("capacite >= 10 AND capacite <= 500"),
    )


class Professeur(Base):
    """Enseignants"""
    __tablename__ = "professeurs"
    
    id = Column(Integer, primary_key=True, index=True)
    matricule = Column(String(20), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    dept_id = Column(Integer, ForeignKey("departements.id", ondelete="RESTRICT"), nullable=False)
    specialite = Column(String(100))
    email = Column(String(150), unique=True, nullable=False)
    telephone = Column(String(20))
    grade = Column(String(50))
    max_surveillances = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    departement = relationship("Departement", back_populates="professeurs")
    examens = relationship("Examen", back_populates="professeur")
    surveillances = relationship("Surveillance", back_populates="professeur")
    
    @property
    def nom_complet(self) -> str:
        return f"{self.prenom} {self.nom}"


class Etudiant(Base):
    """Étudiants"""
    __tablename__ = "etudiants"
    
    id = Column(Integer, primary_key=True, index=True)
    matricule = Column(String(20), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    formation_id = Column(Integer, ForeignKey("formations.id", ondelete="RESTRICT"), nullable=False)
    promo = Column(String(10), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    date_naissance = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    formation = relationship("Formation", back_populates="etudiants")
    inscriptions = relationship("Inscription", back_populates="etudiant")
    
    @property
    def nom_complet(self) -> str:
        return f"{self.prenom} {self.nom}"


class Inscription(Base):
    """Inscriptions étudiants aux modules"""
    __tablename__ = "inscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id", ondelete="CASCADE"), nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    annee_universitaire = Column(String(9), nullable=False, default="2024-2025")
    note = Column(Numeric(4, 2))
    statut = Column(Enum(InscriptionStatus, name="inscription_status", values_callable=lambda x: [e.value for e in x]), default=InscriptionStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    etudiant = relationship("Etudiant", back_populates="inscriptions")
    module = relationship("Module", back_populates="inscriptions")
    
    __table_args__ = (
        UniqueConstraint("etudiant_id", "module_id", "annee_universitaire"),
        CheckConstraint("note >= 0 AND note <= 20"),
    )


class Examen(Base):
    """Planification des examens"""
    __tablename__ = "examens"
    
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"), nullable=False)
    prof_id = Column(Integer, ForeignKey("professeurs.id", ondelete="SET NULL"))
    salle_id = Column(Integer, ForeignKey("lieux_examen.id", ondelete="SET NULL"))
    date_heure = Column(DateTime, nullable=False)
    duree_minutes = Column(Integer, nullable=False)
    statut = Column(Enum(ExamStatus, name="exam_status", values_callable=lambda x: [e.value for e in x]), default=ExamStatus.DRAFT)
    session_id = Column(Integer, ForeignKey("sessions_generation.id", ondelete="SET NULL"))
    nb_inscrits = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    module = relationship("Module", back_populates="examens")
    professeur = relationship("Professeur", back_populates="examens")
    salle = relationship("LieuExamen", back_populates="examens")
    session = relationship("SessionGeneration", back_populates="examens")
    surveillances = relationship("Surveillance", back_populates="examen")
    
    __table_args__ = (
        CheckConstraint("duree_minutes >= 30 AND duree_minutes <= 240"),
    )


class User(Base):
    """Utilisateurs avec authentification"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole, name="user_role", values_callable=lambda x: [e.value for e in x]), nullable=False)
    ref_id = Column(Integer)
    nom = Column(String(100))
    prenom = Column(String(100))
    active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    sessions = relationship("SessionGeneration", back_populates="user")
    
    @property
    def nom_complet(self) -> str:
        return f"{self.prenom} {self.nom}" if self.prenom and self.nom else self.email


class SessionGeneration(Base):
    """Sessions de génération automatique d'EDT"""
    __tablename__ = "sessions_generation"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date_debut = Column(DateTime, default=datetime.utcnow)
    date_fin = Column(DateTime)
    parametres = Column(JSON, default={})
    statut = Column(Enum(SessionStatus, name="session_status", values_callable=lambda x: [e.value for e in x]), default=SessionStatus.PENDING)
    nb_examens_planifies = Column(Integer, default=0)
    nb_conflits_resolus = Column(Integer, default=0)
    temps_execution_ms = Column(Integer)
    log = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="sessions")
    examens = relationship("Examen", back_populates="session")


class Surveillance(Base):
    """Répartition des surveillances"""
    __tablename__ = "surveillances"
    
    id = Column(Integer, primary_key=True, index=True)
    examen_id = Column(Integer, ForeignKey("examens.id", ondelete="CASCADE"), nullable=False)
    prof_id = Column(Integer, ForeignKey("professeurs.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), default="surveillant")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    examen = relationship("Examen", back_populates="surveillances")
    professeur = relationship("Professeur", back_populates="surveillances")
    
    __table_args__ = (
        UniqueConstraint("examen_id", "prof_id"),
        CheckConstraint("role IN ('responsable', 'surveillant')"),
    )
