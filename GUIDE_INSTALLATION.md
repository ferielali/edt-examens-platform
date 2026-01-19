# 🚀 Guide d'Installation - Plateforme EDT Examens

Ce guide explique comment installer et exécuter le projet sur un nouvel ordinateur.

---

## 📋 Prérequis

1. **Node.js** (version 18+) - [Télécharger](https://nodejs.org/)
2. **Python** (version 3.10+) - [Télécharger](https://python.org/)
3. **PostgreSQL** (version 14+) - [Télécharger](https://postgresql.org/download/)

---

## 🗄️ Étape 1 : Configurer la Base de Données

### 1.1 Installer PostgreSQL
- Téléchargez et installez PostgreSQL
- **Notez le mot de passe** que vous choisissez pour l'utilisateur `postgres`

### 1.2 Créer la base de données
Ouvrez **pgAdmin** ou **SQL Shell (psql)** et exécutez :
```sql
CREATE DATABASE exam_scheduler;
```

### 1.3 Importer les données
Dans un terminal (PowerShell ou CMD), exécutez :
```bash
psql -U postgres -d exam_scheduler -f "database/full_backup.sql"
```

> **Note**: Entrez le mot de passe PostgreSQL quand demandé.

**Alternative avec pgAdmin :**
1. Ouvrez pgAdmin
2. Clic droit sur `exam_scheduler` → Query Tool
3. Ouvrez le fichier `database/full_backup.sql`
4. Cliquez sur ▶️ Execute

---

## ⚙️ Étape 2 : Configurer le Backend

### 2.1 Créer le fichier de configuration
Dans le dossier `backend`, copiez `.env.example` vers `.env` :
```bash
cd backend
copy .env.example .env
```

### 2.2 Modifier le fichier `.env`
Ouvrez `backend/.env` et modifiez la ligne `DATABASE_URL` avec votre mot de passe PostgreSQL :
```
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@localhost:5432/exam_scheduler
```

### 2.3 Installer les dépendances Python
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🎨 Étape 3 : Configurer le Frontend

```bash
cd frontend
npm install
```

---

## ▶️ Étape 4 : Lancer le Projet

### Terminal 1 - Backend :
```bash
cd backend
.\venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

### Terminal 2 - Frontend :
```bash
cd frontend
npm run dev
```

---

## 🌐 Étape 5 : Accéder à l'Application

Ouvrez votre navigateur et allez à : **http://localhost:3000**

---

## 🔐 Comptes de Connexion

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| Directeur | admin@univ.edu | admin123 |

---

## ❓ Problèmes Courants

### "Connection refused" ou "Database not found"
- Vérifiez que PostgreSQL est démarré
- Vérifiez le mot de passe dans `.env`

### "Module not found" (Backend)
```bash
pip install -r requirements.txt
```

### "npm ERR!" (Frontend)
```bash
npm install
```

---

## 📁 Structure du Projet

```
Projet de fifi/
├── backend/          # API FastAPI (Python)
├── frontend/         # Interface React (TypeScript)
├── database/         # Scripts SQL
│   ├── schema.sql    # Structure des tables
│   └── full_backup.sql  # Données complètes
└── GUIDE_INSTALLATION.md
```

---

**Bonne installation ! 🎉**
