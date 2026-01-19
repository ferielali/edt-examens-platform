"""
Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires
Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.api import auth_router, examens_router, dashboard_router

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
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
