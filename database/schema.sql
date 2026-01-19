-- ============================================================================
-- PLATEFORME D'OPTIMISATION DES EMPLOIS DU TEMPS D'EXAMENS UNIVERSITAIRES
-- Script de création de la base de données PostgreSQL
-- ============================================================================

-- Création de la base de données (exécuter séparément si nécessaire)
-- CREATE DATABASE exam_scheduler;

-- ============================================================================
-- EXTENSIONS
-- ============================================================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- TYPES ÉNUMÉRÉS
-- ============================================================================
CREATE TYPE user_role AS ENUM ('director', 'administrator', 'department_head', 'professor', 'student');
CREATE TYPE exam_status AS ENUM ('draft', 'scheduled', 'confirmed', 'completed', 'cancelled');
CREATE TYPE inscription_status AS ENUM ('active', 'withdrawn', 'completed');
CREATE TYPE room_type AS ENUM ('amphi', 'salle_td', 'salle_tp', 'salle_info');
CREATE TYPE session_status AS ENUM ('pending', 'in_progress', 'completed', 'failed');

-- ============================================================================
-- TABLE: DEPARTEMENTS
-- ============================================================================
CREATE TABLE departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    code VARCHAR(10) NOT NULL UNIQUE,
    batiment VARCHAR(50),
    telephone VARCHAR(20),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_departements_code ON departements(code);

COMMENT ON TABLE departements IS 'Départements universitaires (7 au total)';

-- ============================================================================
-- TABLE: FORMATIONS
-- ============================================================================
CREATE TABLE formations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    dept_id INTEGER NOT NULL REFERENCES departements(id) ON DELETE RESTRICT,
    nb_modules INTEGER DEFAULT 0,
    niveau VARCHAR(20) CHECK (niveau IN ('L1', 'L2', 'L3', 'M1', 'M2', 'D')),
    type_formation VARCHAR(50) CHECK (type_formation IN ('licence', 'master', 'doctorat')),
    capacite_max INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_formations_dept ON formations(dept_id);
CREATE INDEX idx_formations_niveau ON formations(niveau);

COMMENT ON TABLE formations IS 'Formations académiques (200+ au total)';

-- ============================================================================
-- TABLE: MODULES
-- ============================================================================
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    formation_id INTEGER NOT NULL REFERENCES formations(id) ON DELETE CASCADE,
    credits INTEGER DEFAULT 3 CHECK (credits >= 1 AND credits <= 10),
    semestre INTEGER CHECK (semestre >= 1 AND semestre <= 2),
    pre_req_id INTEGER REFERENCES modules(id) ON DELETE SET NULL,
    duree_examen_min INTEGER DEFAULT 120 CHECK (duree_examen_min >= 30 AND duree_examen_min <= 240),
    coefficient DECIMAL(3,1) DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_modules_formation ON modules(formation_id);
CREATE INDEX idx_modules_semestre ON modules(semestre);

COMMENT ON TABLE modules IS 'Modules/Matières par formation (6-9 modules par formation)';

-- ============================================================================
-- TABLE: LIEUX_EXAMEN
-- ============================================================================
CREATE TABLE lieux_examen (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    capacite INTEGER NOT NULL CHECK (capacite >= 10 AND capacite <= 500),
    capacite_examen INTEGER GENERATED ALWAYS AS (capacite / 2) STORED,
    type room_type NOT NULL DEFAULT 'salle_td',
    batiment VARCHAR(50) NOT NULL,
    etage INTEGER DEFAULT 0,
    disponible BOOLEAN DEFAULT TRUE,
    equipements JSONB DEFAULT '{}',
    accessibilite_pmr BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lieux_type ON lieux_examen(type);
CREATE INDEX idx_lieux_batiment ON lieux_examen(batiment);
CREATE INDEX idx_lieux_disponible ON lieux_examen(disponible) WHERE disponible = TRUE;

COMMENT ON TABLE lieux_examen IS 'Salles d''examen avec capacité réduite de moitié pour examens';
COMMENT ON COLUMN lieux_examen.capacite_examen IS 'Capacité réelle pendant examens (max 20 étudiants en période normale)';

-- ============================================================================
-- TABLE: PROFESSEURS
-- ============================================================================
CREATE TABLE professeurs (
    id SERIAL PRIMARY KEY,
    matricule VARCHAR(20) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dept_id INTEGER NOT NULL REFERENCES departements(id) ON DELETE RESTRICT,
    specialite VARCHAR(100),
    email VARCHAR(150) NOT NULL UNIQUE,
    telephone VARCHAR(20),
    grade VARCHAR(50) CHECK (grade IN ('MCF', 'PR', 'ATER', 'Vacataire', 'PRAG')),
    max_surveillances INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_professeurs_dept ON professeurs(dept_id);
CREATE INDEX idx_professeurs_email ON professeurs(email);

COMMENT ON TABLE professeurs IS 'Enseignants et surveillants - Max 3 examens/jour';

-- ============================================================================
-- TABLE: ETUDIANTS
-- ============================================================================
CREATE TABLE etudiants (
    id SERIAL PRIMARY KEY,
    matricule VARCHAR(20) NOT NULL UNIQUE,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    formation_id INTEGER NOT NULL REFERENCES formations(id) ON DELETE RESTRICT,
    promo VARCHAR(10) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    date_naissance DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_etudiants_formation ON etudiants(formation_id);
CREATE INDEX idx_etudiants_promo ON etudiants(promo);
CREATE INDEX idx_etudiants_email ON etudiants(email);

COMMENT ON TABLE etudiants IS 'Étudiants inscrits (13 000+ au total)';

-- ============================================================================
-- TABLE: INSCRIPTIONS
-- ============================================================================
CREATE TABLE inscriptions (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiants(id) ON DELETE CASCADE,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    annee_universitaire VARCHAR(9) NOT NULL DEFAULT '2024-2025',
    note DECIMAL(4,2) CHECK (note >= 0 AND note <= 20),
    statut inscription_status DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(etudiant_id, module_id, annee_universitaire)
);

CREATE INDEX idx_inscriptions_etudiant ON inscriptions(etudiant_id);
CREATE INDEX idx_inscriptions_module ON inscriptions(module_id);
CREATE INDEX idx_inscriptions_annee ON inscriptions(annee_universitaire);
CREATE INDEX idx_inscriptions_statut ON inscriptions(statut) WHERE statut = 'active';

COMMENT ON TABLE inscriptions IS 'Inscriptions étudiants aux modules (130k+ inscriptions)';

-- ============================================================================
-- TABLE: EXAMENS
-- ============================================================================
CREATE TABLE examens (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    prof_id INTEGER REFERENCES professeurs(id) ON DELETE SET NULL,
    salle_id INTEGER REFERENCES lieux_examen(id) ON DELETE SET NULL,
    date_heure TIMESTAMP NOT NULL,
    duree_minutes INTEGER NOT NULL CHECK (duree_minutes >= 30 AND duree_minutes <= 240),
    statut exam_status DEFAULT 'draft',
    session_id INTEGER,
    nb_inscrits INTEGER DEFAULT 0,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_examens_module ON examens(module_id);
CREATE INDEX idx_examens_prof ON examens(prof_id);
CREATE INDEX idx_examens_salle ON examens(salle_id);
CREATE INDEX idx_examens_date ON examens(date_heure);
CREATE INDEX idx_examens_statut ON examens(statut);
CREATE INDEX idx_examens_session ON examens(session_id);

COMMENT ON TABLE examens IS 'Planification des examens avec contraintes';

-- ============================================================================
-- TABLE: USERS (Authentification)
-- ============================================================================
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL,
    ref_id INTEGER,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(active) WHERE active = TRUE;

COMMENT ON TABLE users IS 'Utilisateurs avec authentification JWT et rôles';

-- ============================================================================
-- TABLE: SESSIONS_GENERATION
-- ============================================================================
CREATE TABLE sessions_generation (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date_debut TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_fin TIMESTAMP,
    parametres JSONB DEFAULT '{}',
    statut session_status DEFAULT 'pending',
    nb_examens_planifies INTEGER DEFAULT 0,
    nb_conflits_resolus INTEGER DEFAULT 0,
    temps_execution_ms INTEGER,
    log TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user ON sessions_generation(user_id);
CREATE INDEX idx_sessions_statut ON sessions_generation(statut);

COMMENT ON TABLE sessions_generation IS 'Sessions de génération automatique d''EDT';

-- ============================================================================
-- TABLE: SURVEILLANCES (Table de liaison pour répartition équitable)
-- ============================================================================
CREATE TABLE surveillances (
    id SERIAL PRIMARY KEY,
    examen_id INTEGER NOT NULL REFERENCES examens(id) ON DELETE CASCADE,
    prof_id INTEGER NOT NULL REFERENCES professeurs(id) ON DELETE CASCADE,
    role VARCHAR(20) DEFAULT 'surveillant' CHECK (role IN ('responsable', 'surveillant')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(examen_id, prof_id)
);

CREATE INDEX idx_surveillances_examen ON surveillances(examen_id);
CREATE INDEX idx_surveillances_prof ON surveillances(prof_id);

COMMENT ON TABLE surveillances IS 'Répartition équitable des surveillances entre enseignants';

-- ============================================================================
-- CONTRAINTES MÉTIER (Fonctions et Triggers)
-- ============================================================================

-- Fonction: Vérifier qu'un étudiant n'a pas plus d'1 examen par jour
CREATE OR REPLACE FUNCTION check_student_exam_per_day()
RETURNS TRIGGER AS $$
DECLARE
    conflict_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO conflict_count
    FROM examens e
    JOIN inscriptions i ON i.module_id = e.module_id
    WHERE i.etudiant_id IN (
        SELECT etudiant_id FROM inscriptions WHERE module_id = NEW.module_id
    )
    AND DATE(e.date_heure) = DATE(NEW.date_heure)
    AND e.id != COALESCE(NEW.id, 0)
    AND e.statut NOT IN ('cancelled', 'draft');
    
    IF conflict_count > 0 THEN
        RAISE WARNING 'Conflit détecté: % étudiant(s) ont déjà un examen ce jour', conflict_count;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Fonction: Vérifier qu'un professeur n'a pas plus de 3 examens par jour
CREATE OR REPLACE FUNCTION check_professor_exam_limit()
RETURNS TRIGGER AS $$
DECLARE
    exam_count INTEGER;
BEGIN
    IF NEW.prof_id IS NOT NULL THEN
        SELECT COUNT(*) INTO exam_count
        FROM examens
        WHERE prof_id = NEW.prof_id
        AND DATE(date_heure) = DATE(NEW.date_heure)
        AND id != COALESCE(NEW.id, 0)
        AND statut NOT IN ('cancelled', 'draft');
        
        IF exam_count >= 3 THEN
            RAISE EXCEPTION 'Le professeur a déjà 3 examens planifiés ce jour';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Fonction: Vérifier la capacité de la salle
CREATE OR REPLACE FUNCTION check_room_capacity()
RETURNS TRIGGER AS $$
DECLARE
    room_capacity INTEGER;
    student_count INTEGER;
BEGIN
    IF NEW.salle_id IS NOT NULL THEN
        SELECT capacite_examen INTO room_capacity
        FROM lieux_examen WHERE id = NEW.salle_id;
        
        SELECT COUNT(*) INTO student_count
        FROM inscriptions WHERE module_id = NEW.module_id AND statut = 'active';
        
        IF student_count > room_capacity THEN
            RAISE WARNING 'Capacité insuffisante: % étudiants pour % places', student_count, room_capacity;
        END IF;
        
        NEW.nb_inscrits := student_count;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Fonction: Vérifier les chevauchements horaires pour une salle
CREATE OR REPLACE FUNCTION check_room_overlap()
RETURNS TRIGGER AS $$
DECLARE
    overlap_count INTEGER;
BEGIN
    IF NEW.salle_id IS NOT NULL AND NEW.date_heure IS NOT NULL THEN
        SELECT COUNT(*) INTO overlap_count
        FROM examens
        WHERE salle_id = NEW.salle_id
        AND id != COALESCE(NEW.id, 0)
        AND statut NOT IN ('cancelled', 'draft')
        AND (
            (NEW.date_heure, NEW.date_heure + (NEW.duree_minutes || ' minutes')::INTERVAL)
            OVERLAPS
            (date_heure, date_heure + (duree_minutes || ' minutes')::INTERVAL)
        );
        
        IF overlap_count > 0 THEN
            RAISE EXCEPTION 'La salle est déjà occupée pendant ce créneau';
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Application des triggers
CREATE TRIGGER trg_check_student_exam
    BEFORE INSERT OR UPDATE ON examens
    FOR EACH ROW EXECUTE FUNCTION check_student_exam_per_day();

CREATE TRIGGER trg_check_professor_limit
    BEFORE INSERT OR UPDATE ON examens
    FOR EACH ROW EXECUTE FUNCTION check_professor_exam_limit();

CREATE TRIGGER trg_check_room_capacity
    BEFORE INSERT OR UPDATE ON examens
    FOR EACH ROW EXECUTE FUNCTION check_room_capacity();

CREATE TRIGGER trg_check_room_overlap
    BEFORE INSERT OR UPDATE ON examens
    FOR EACH ROW EXECUTE FUNCTION check_room_overlap();

-- ============================================================================
-- FONCTIONS UTILITAIRES
-- ============================================================================

-- Fonction: Mise à jour automatique de updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Appliquer sur toutes les tables
CREATE TRIGGER update_departements_updated_at BEFORE UPDATE ON departements
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_formations_updated_at BEFORE UPDATE ON formations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_modules_updated_at BEFORE UPDATE ON modules
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_lieux_updated_at BEFORE UPDATE ON lieux_examen
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_professeurs_updated_at BEFORE UPDATE ON professeurs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_etudiants_updated_at BEFORE UPDATE ON etudiants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_inscriptions_updated_at BEFORE UPDATE ON inscriptions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_examens_updated_at BEFORE UPDATE ON examens
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VUES POUR LE DASHBOARD
-- ============================================================================

-- Vue: Statistiques par département
CREATE OR REPLACE VIEW v_stats_departement AS
SELECT 
    d.id,
    d.nom,
    d.code,
    COUNT(DISTINCT f.id) as nb_formations,
    COUNT(DISTINCT m.id) as nb_modules,
    COUNT(DISTINCT p.id) as nb_professeurs,
    COUNT(DISTINCT e.id) as nb_etudiants
FROM departements d
LEFT JOIN formations f ON f.dept_id = d.id
LEFT JOIN modules m ON m.formation_id = f.id
LEFT JOIN professeurs p ON p.dept_id = d.id
LEFT JOIN etudiants e ON e.formation_id = f.id
GROUP BY d.id, d.nom, d.code;

-- Vue: Conflits potentiels
CREATE OR REPLACE VIEW v_conflits_examens AS
SELECT 
    e1.id as examen1_id,
    e2.id as examen2_id,
    e1.date_heure,
    'chevauchement_salle' as type_conflit,
    l.nom as salle
FROM examens e1
JOIN examens e2 ON e1.salle_id = e2.salle_id 
    AND e1.id < e2.id
    AND e1.statut NOT IN ('cancelled', 'draft')
    AND e2.statut NOT IN ('cancelled', 'draft')
JOIN lieux_examen l ON l.id = e1.salle_id
WHERE (e1.date_heure, e1.date_heure + (e1.duree_minutes || ' minutes')::INTERVAL)
    OVERLAPS (e2.date_heure, e2.date_heure + (e2.duree_minutes || ' minutes')::INTERVAL);

-- Vue: Occupation des salles
CREATE OR REPLACE VIEW v_occupation_salles AS
SELECT 
    l.id,
    l.nom,
    l.code,
    l.capacite_examen,
    l.type,
    l.batiment,
    COUNT(e.id) as nb_examens_planifies,
    SUM(COALESCE(e.nb_inscrits, 0)) as total_etudiants
FROM lieux_examen l
LEFT JOIN examens e ON e.salle_id = l.id AND e.statut NOT IN ('cancelled', 'draft')
GROUP BY l.id, l.nom, l.code, l.capacite_examen, l.type, l.batiment;

-- Vue: Planning professeur
CREATE OR REPLACE VIEW v_planning_professeur AS
SELECT 
    p.id as prof_id,
    p.nom,
    p.prenom,
    p.matricule,
    e.id as examen_id,
    m.nom as module_nom,
    e.date_heure,
    e.duree_minutes,
    l.nom as salle,
    e.statut
FROM professeurs p
JOIN examens e ON e.prof_id = p.id
JOIN modules m ON m.id = e.module_id
LEFT JOIN lieux_examen l ON l.id = e.salle_id
ORDER BY p.id, e.date_heure;

-- Vue: Planning étudiant
CREATE OR REPLACE VIEW v_planning_etudiant AS
SELECT 
    et.id as etudiant_id,
    et.nom,
    et.prenom,
    et.matricule,
    e.id as examen_id,
    m.nom as module_nom,
    e.date_heure,
    e.duree_minutes,
    l.nom as salle,
    l.batiment,
    e.statut
FROM etudiants et
JOIN inscriptions i ON i.etudiant_id = et.id AND i.statut = 'active'
JOIN modules m ON m.id = i.module_id
JOIN examens e ON e.module_id = m.id
LEFT JOIN lieux_examen l ON l.id = e.salle_id
ORDER BY et.id, e.date_heure;

-- ============================================================================
-- INDEX PARTIELS POUR OPTIMISATION
-- ============================================================================
CREATE INDEX idx_examens_actifs ON examens(date_heure, salle_id) 
    WHERE statut IN ('scheduled', 'confirmed');

CREATE INDEX idx_inscriptions_actives ON inscriptions(etudiant_id, module_id) 
    WHERE statut = 'active';

-- ============================================================================
-- DONNÉES INITIALES (Utilisateur admin)
-- ============================================================================
INSERT INTO users (email, password_hash, role, nom, prenom, active)
VALUES (
    'admin@univ.edu',
    crypt('admin123', gen_salt('bf')),
    'director',
    'Admin',
    'System',
    TRUE
);

COMMENT ON DATABASE exam_scheduler IS 'Base de données pour la plateforme d''optimisation des EDT d''examens universitaires';
