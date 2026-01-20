"""
Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api import auth_router, examens_router, dashboard_router
from app.core.database import engine, SessionLocal, Base
from app.models import User, UserRole
from app.core.security import get_password_hash


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    Creates database tables and seeds admin user if not exists.
    """
    # Startup: Create tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # Seed users for all roles if they don't exist
    users_to_seed = [
        {
            "email": "admin@univ.edu",
            "password": "Director123!",
            "role": UserRole.DIRECTOR,
            "nom": "Administrateur",
            "prenom": "Principal"
        },
        {
            "email": "admin.scolarite@univ.edu",
            "password": "Admin123!",
            "role": UserRole.ADMINISTRATOR,
            "nom": "Martin",
            "prenom": "Sophie"
        },
        {
            "email": "chef.info@univ.edu",
            "password": "Chef123!",
            "role": UserRole.DEPARTMENT_HEAD,
            "nom": "Dupont",
            "prenom": "Jean"
        },
        {
            "email": "prof.math@univ.edu",
            "password": "Prof123!",
            "role": UserRole.PROFESSOR,
            "nom": "Bernard",
            "prenom": "Marie"
        },
        {
            "email": "etudiant@univ.edu",
            "password": "Etudiant123!",
            "role": UserRole.STUDENT,
            "nom": "Petit",
            "prenom": "Lucas"
        }
    ]
    
    db = SessionLocal()
    try:
        for user_data in users_to_seed:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                print(f"Creating user: {user_data['email']} ({user_data['role'].value})...")
                new_user = User(
                    email=user_data["email"],
                    password_hash=get_password_hash(user_data["password"]),
                    role=user_data["role"],
                    nom=user_data["nom"],
                    prenom=user_data["prenom"],
                    active=True
                )
                db.add(new_user)
                db.commit()
                print(f"User created: {user_data['email']} / {user_data['password']}")
            else:
                print(f"User already exists: {existing_user.email}")
    except Exception as e:
        print(f"Error seeding admin user: {e}")
        db.rollback()
    finally:
        db.close()
    
    yield
    # Shutdown
    print("Shutting down...")

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    description="""
    ## Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires
    
    API REST pour la gestion et l'optimisation automatique des plannings d'examens.
    
    ### Fonctionnalités principales:
    - 🔐 **Authentification JWT** avec gestion des rôles
    - 📅 **Génération automatique d'EDT** avec algorithme d'optimisation OR-Tools
    - 👥 **Gestion multi-rôles** (Directeur, Administrateur, Chef département, Professeur, Étudiant)
    - 📊 **Dashboard et KPIs** en temps réel
    - ⚠️ **Détection de conflits** automatique
    
    ### Contraintes respectées:
    - Maximum 1 examen par jour par étudiant
    - Maximum 3 surveillances par jour par professeur
    - Respect des capacités des salles
    - Priorisation des examens par département
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Authentication", "description": "Authentification et gestion des tokens JWT"},
        {"name": "Examens", "description": "Gestion des examens et génération d'EDT"},
        {"name": "Dashboard", "description": "Statistiques et KPIs"},
    ]
)

# Configure CORS - Allow all origins for Railway deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api")
app.include_router(examens_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


@app.get("/", tags=["Root"])
async def root():
    """
    Point d'entrée de l'API.
    """
    return {
        "message": "Bienvenue sur l'API de la Plateforme d'Optimisation des EDT d'Examens",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Vérification de l'état de l'API.
    """
    return {"status": "healthy", "version": settings.APP_VERSION}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Gestionnaire global des exceptions.
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erreur interne du serveur",
            "message": str(exc) if settings.DEBUG else "Une erreur inattendue s'est produite"
        }
    )


# Application entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
