"""Schemas module exports"""
from app.schemas.schemas import (
    # Enums
    UserRoleEnum,
    ExamStatusEnum,
    RoomTypeEnum,
    # Auth
    Token,
    TokenData,
    LoginRequest,
    RefreshRequest,
    # User
    UserBase,
    UserCreate,
    UserResponse,
    UserProfile,
    # Departement
    DepartementBase,
    DepartementCreate,
    DepartementResponse,
    DepartementStats,
    # Formation
    FormationBase,
    FormationCreate,
    FormationResponse,
    # Module
    ModuleBase,
    ModuleCreate,
    ModuleResponse,
    # Lieu Examen
    LieuExamenBase,
    LieuExamenCreate,
    LieuExamenResponse,
    # Professeur
    ProfesseurBase,
    ProfesseurCreate,
    ProfesseurResponse,
    # Etudiant
    EtudiantBase,
    EtudiantCreate,
    EtudiantResponse,
    # Inscription
    InscriptionBase,
    InscriptionCreate,
    InscriptionResponse,
    # Examen
    ExamenBase,
    ExamenCreate,
    ExamenUpdate,
    ExamenResponse,
    # EDT Generation
    EDTGenerationRequest,
    EDTGenerationResponse,
    ConflictInfo,
    # Statistics
    DashboardStats,
    DepartementKPI,
    # Pagination
    PaginationParams,
    PaginatedResponse
)

__all__ = [
    "UserRoleEnum",
    "ExamStatusEnum",
    "RoomTypeEnum",
    "Token",
    "TokenData",
    "LoginRequest",
    "RefreshRequest",
    "UserBase",
    "UserCreate",
    "UserResponse",
    "UserProfile",
    "DepartementBase",
    "DepartementCreate",
    "DepartementResponse",
    "DepartementStats",
    "FormationBase",
    "FormationCreate",
    "FormationResponse",
    "ModuleBase",
    "ModuleCreate",
    "ModuleResponse",
    "LieuExamenBase",
    "LieuExamenCreate",
    "LieuExamenResponse",
    "ProfesseurBase",
    "ProfesseurCreate",
    "ProfesseurResponse",
    "EtudiantBase",
    "EtudiantCreate",
    "EtudiantResponse",
    "InscriptionBase",
    "InscriptionCreate",
    "InscriptionResponse",
    "ExamenBase",
    "ExamenCreate",
    "ExamenUpdate",
    "ExamenResponse",
    "EDTGenerationRequest",
    "EDTGenerationResponse",
    "ConflictInfo",
    "DashboardStats",
    "DepartementKPI",
    "PaginationParams",
    "PaginatedResponse"
]
