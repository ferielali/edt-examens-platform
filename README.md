# Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires

Application web professionnelle pour la gestion et l'optimisation automatique des plannings d'examens universitaires.

## 🚀 Fonctionnalités

- **Génération automatique d'EDT** avec algorithme OR-Tools (< 45 secondes)
- **Gestion multi-rôles** : Directeur, Administrateur, Chef de département, Professeur, Étudiant
- **Détection de conflits** en temps réel
- **Dashboard analytique** avec KPIs
- **API REST sécurisée** avec JWT

## 📋 Prérequis

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

## 🛠️ Installation

### 1. Base de données

```bash
# Créer la base de données
createdb exam_scheduler

# Exécuter le schéma
psql -d exam_scheduler -f database/schema.sql

# Insérer les données de test
psql -d exam_scheduler -f database/seed_data.sql
```

### 2. Backend

```bash
cd backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm run dev
```

## 🔐 Comptes de Démonstration

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Directeur | directeur@univ.edu | Director123! |
| Administrateur | admin.examens@univ.edu | Admin123! |
| Chef Département | chef.info@univ.edu | Chef123! |

## 📁 Structure du Projet

```
exam-scheduler/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/            # Endpoints REST
│   │   ├── core/           # Config, security
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Logique métier
│   └── requirements.txt
├── frontend/               # React + Ant Design
│   ├── src/
│   │   ├── components/     # Composants réutilisables
│   │   ├── pages/          # Pages dashboards
│   │   ├── services/       # API calls
│   │   └── context/        # Auth context
│   └── package.json
├── database/               # Scripts SQL
│   ├── schema.sql
│   └── seed_data.sql
└── docs/                   # Documentation
```

## 📊 API Documentation

Une fois le backend lancé, accédez à:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Tests

```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test
```

## 📈 Performances

- Génération EDT: < 45 secondes pour 130k+ inscriptions
- Temps de réponse API: < 100ms
- Support: 13 000+ étudiants, 200+ formations

## 📝 Licence

Projet académique - Tous droits réservés.
