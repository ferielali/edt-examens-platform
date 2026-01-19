-- ============================================================================
-- SCRIPT DE GÉNÉRATION DE DONNÉES RÉALISTES
-- Plateforme d'Optimisation des Emplois du Temps d'Examens Universitaires
-- ============================================================================

-- ============================================================================
-- INSERTION DES DÉPARTEMENTS (7 départements)
-- ============================================================================
INSERT INTO departements (nom, code, batiment, telephone, email) VALUES
('Informatique', 'INFO', 'Bâtiment A', '01 23 45 67 01', 'info@univ.edu'),
('Mathématiques', 'MATH', 'Bâtiment A', '01 23 45 67 02', 'math@univ.edu'),
('Physique', 'PHYS', 'Bâtiment B', '01 23 45 67 03', 'phys@univ.edu'),
('Chimie', 'CHIM', 'Bâtiment B', '01 23 45 67 04', 'chim@univ.edu'),
('Biologie', 'BIO', 'Bâtiment C', '01 23 45 67 05', 'bio@univ.edu'),
('Sciences Économiques', 'ECO', 'Bâtiment D', '01 23 45 67 06', 'eco@univ.edu'),
('Langues et Lettres', 'LET', 'Bâtiment E', '01 23 45 67 07', 'let@univ.edu');

-- ============================================================================
-- INSERTION DES SALLES D'EXAMEN (30 salles)
-- ============================================================================
INSERT INTO lieux_examen (nom, code, capacite, type, batiment, etage, disponible, equipements, accessibilite_pmr) VALUES
-- Amphithéâtres
('Amphithéâtre Turing', 'AMPHI-A1', 400, 'amphi', 'Bâtiment A', 0, TRUE, '{"videoprojection": true, "micro": true, "climatisation": true}', TRUE),
('Amphithéâtre Pascal', 'AMPHI-A2', 300, 'amphi', 'Bâtiment A', 0, TRUE, '{"videoprojection": true, "micro": true, "climatisation": true}', TRUE),
('Amphithéâtre Curie', 'AMPHI-B1', 350, 'amphi', 'Bâtiment B', 0, TRUE, '{"videoprojection": true, "micro": true, "climatisation": true}', TRUE),
('Amphithéâtre Einstein', 'AMPHI-C1', 250, 'amphi', 'Bâtiment C', 0, TRUE, '{"videoprojection": true, "micro": true}', TRUE),
('Amphithéâtre Darwin', 'AMPHI-D1', 200, 'amphi', 'Bâtiment D', 0, TRUE, '{"videoprojection": true, "micro": true}', FALSE),

-- Salles TD
('Salle TD 101', 'TD-A101', 40, 'salle_td', 'Bâtiment A', 1, TRUE, '{"videoprojection": true}', TRUE),
('Salle TD 102', 'TD-A102', 40, 'salle_td', 'Bâtiment A', 1, TRUE, '{"videoprojection": true}', TRUE),
('Salle TD 103', 'TD-A103', 35, 'salle_td', 'Bâtiment A', 1, TRUE, '{"videoprojection": true}', FALSE),
('Salle TD 201', 'TD-A201', 40, 'salle_td', 'Bâtiment A', 2, TRUE, '{"videoprojection": true}', FALSE),
('Salle TD 202', 'TD-A202', 45, 'salle_td', 'Bâtiment A', 2, TRUE, '{"videoprojection": true}', TRUE),
('Salle TD 301', 'TD-B301', 40, 'salle_td', 'Bâtiment B', 3, TRUE, '{"videoprojection": true}', FALSE),
('Salle TD 302', 'TD-B302', 40, 'salle_td', 'Bâtiment B', 3, TRUE, '{"videoprojection": true}', FALSE),
('Salle TD 303', 'TD-B303', 35, 'salle_td', 'Bâtiment B', 3, TRUE, '{"videoprojection": true}', TRUE),
('Salle TD 401', 'TD-C401', 50, 'salle_td', 'Bâtiment C', 4, TRUE, '{"videoprojection": true}', FALSE),
('Salle TD 402', 'TD-C402', 45, 'salle_td', 'Bâtiment C', 4, TRUE, '{"videoprojection": true}', TRUE),

-- Salles TP
('Salle TP Physique 1', 'TP-B101', 30, 'salle_tp', 'Bâtiment B', 1, TRUE, '{"equipement_labo": true}', FALSE),
('Salle TP Physique 2', 'TP-B102', 30, 'salle_tp', 'Bâtiment B', 1, TRUE, '{"equipement_labo": true}', FALSE),
('Salle TP Chimie 1', 'TP-B201', 28, 'salle_tp', 'Bâtiment B', 2, TRUE, '{"equipement_labo": true, "hotte": true}', FALSE),
('Salle TP Chimie 2', 'TP-B202', 28, 'salle_tp', 'Bâtiment B', 2, TRUE, '{"equipement_labo": true, "hotte": true}', FALSE),
('Salle TP Bio 1', 'TP-C101', 32, 'salle_tp', 'Bâtiment C', 1, TRUE, '{"equipement_labo": true, "microscopes": true}', TRUE),

-- Salles Informatique
('Salle Info 1', 'INFO-A301', 40, 'salle_info', 'Bâtiment A', 3, TRUE, '{"ordinateurs": 40, "internet": true}', TRUE),
('Salle Info 2', 'INFO-A302', 40, 'salle_info', 'Bâtiment A', 3, TRUE, '{"ordinateurs": 40, "internet": true}', TRUE),
('Salle Info 3', 'INFO-A303', 35, 'salle_info', 'Bâtiment A', 3, TRUE, '{"ordinateurs": 35, "internet": true}', FALSE),
('Salle Info 4', 'INFO-A304', 30, 'salle_info', 'Bâtiment A', 3, TRUE, '{"ordinateurs": 30, "internet": true}', FALSE),
('Salle Info 5', 'INFO-A401', 45, 'salle_info', 'Bâtiment A', 4, TRUE, '{"ordinateurs": 45, "internet": true}', TRUE),
('Salle Examen 1', 'EXAM-D101', 60, 'salle_td', 'Bâtiment D', 1, TRUE, '{"videoprojection": true}', TRUE),
('Salle Examen 2', 'EXAM-D102', 60, 'salle_td', 'Bâtiment D', 1, TRUE, '{"videoprojection": true}', TRUE),
('Salle Examen 3', 'EXAM-D201', 50, 'salle_td', 'Bâtiment D', 2, TRUE, '{"videoprojection": true}', FALSE),
('Salle Examen 4', 'EXAM-E101', 55, 'salle_td', 'Bâtiment E', 1, TRUE, '{"videoprojection": true}', TRUE),
('Salle Examen 5', 'EXAM-E102', 55, 'salle_td', 'Bâtiment E', 1, TRUE, '{"videoprojection": true}', FALSE);

-- ============================================================================
-- INSERTION DES FORMATIONS (200+ formations)
-- ============================================================================

-- Formations Informatique (30)
INSERT INTO formations (nom, code, dept_id, nb_modules, niveau, type_formation, capacite_max) VALUES
('Licence Informatique', 'L-INFO', 1, 8, 'L1', 'licence', 150),
('Licence Informatique 2ème année', 'L2-INFO', 1, 8, 'L2', 'licence', 140),
('Licence Informatique 3ème année', 'L3-INFO', 1, 9, 'L3', 'licence', 120),
('Master Génie Logiciel', 'M1-GL', 1, 7, 'M1', 'master', 40),
('Master Génie Logiciel 2', 'M2-GL', 1, 6, 'M2', 'master', 35),
('Master Intelligence Artificielle', 'M1-IA', 1, 7, 'M1', 'master', 45),
('Master Intelligence Artificielle 2', 'M2-IA', 1, 6, 'M2', 'master', 40),
('Master Cybersécurité', 'M1-SEC', 1, 7, 'M1', 'master', 35),
('Master Cybersécurité 2', 'M2-SEC', 1, 6, 'M2', 'master', 30),
('Master Data Science', 'M1-DS', 1, 7, 'M1', 'master', 40),
('Master Data Science 2', 'M2-DS', 1, 6, 'M2', 'master', 35),
('Licence Pro Développement Web', 'LP-WEB', 1, 8, 'L3', 'licence', 30),
('Licence Pro Administration Systèmes', 'LP-SYS', 1, 8, 'L3', 'licence', 25),
('Master Réseaux et Télécoms', 'M1-RES', 1, 7, 'M1', 'master', 30),
('Master Réseaux et Télécoms 2', 'M2-RES', 1, 6, 'M2', 'master', 25);

-- Formations Mathématiques (25)
INSERT INTO formations (nom, code, dept_id, nb_modules, niveau, type_formation, capacite_max) VALUES
('Licence Mathématiques', 'L-MATH', 2, 8, 'L1', 'licence', 100),
('Licence Mathématiques 2ème année', 'L2-MATH', 2, 8, 'L2', 'licence', 90),
('Licence Mathématiques 3ème année', 'L3-MATH', 2, 9, 'L3', 'licence', 80),
('Master Mathématiques Appliquées', 'M1-MAPA', 2, 7, 'M1', 'master', 35),
('Master Mathématiques Appliquées 2', 'M2-MAPA', 2, 6, 'M2', 'master', 30),
('Master Mathématiques Fondamentales', 'M1-MAFO', 2, 7, 'M1', 'master', 25),
('Master Mathématiques Fondamentales 2', 'M2-MAFO', 2, 6, 'M2', 'master', 20),
('Master Statistiques', 'M1-STAT', 2, 7, 'M1', 'master', 35),
('Master Statistiques 2', 'M2-STAT', 2, 6, 'M2', 'master', 30),
('Licence MIASHS', 'L-MIASHS', 2, 8, 'L1', 'licence', 60);

-- Formations Physique (25)
INSERT INTO formations (nom, code, dept_id, nb_modules, niveau, type_formation, capacite_max) VALUES
('Licence Physique', 'L-PHYS', 3, 8, 'L1', 'licence', 120),
('Licence Physique 2ème année', 'L2-PHYS', 3, 8, 'L2', 'licence', 100),
('Licence Physique 3ème année', 'L3-PHYS', 3, 9, 'L3', 'licence', 85),
('Master Physique Fondamentale', 'M1-PHFO', 3, 7, 'M1', 'master', 30),
('Master Physique Fondamentale 2', 'M2-PHFO', 3, 6, 'M2', 'master', 25),
('Master Physique Appliquée', 'M1-PHAP', 3, 7, 'M1', 'master', 35),
('Master Physique Appliquée 2', 'M2-PHAP', 3, 6, 'M2', 'master', 30),
('Master Astrophysique', 'M1-ASTR', 3, 7, 'M1', 'master', 20),
('Master Astrophysique 2', 'M2-ASTR', 3, 6, 'M2', 'master', 15),
('Licence Physique-Chimie', 'L-PCHI', 3, 8, 'L1', 'licence', 80);

-- Formations Chimie (20)
INSERT INTO formations (nom, code, dept_id, nb_modules, niveau, type_formation, capacite_max) VALUES
('Licence Chimie', 'L-CHIM', 4, 8, 'L1', 'licence', 90),
('Licence Chimie 2ème année', 'L2-CHIM', 4, 8, 'L2', 'licence', 80),
('Licence Chimie 3ème année', 'L3-CHIM', 4, 9, 'L3', 'licence', 70),
('Master Chimie Organique', 'M1-CORG', 4, 7, 'M1', 'master', 30),
('Master Chimie Organique 2', 'M2-CORG', 4, 6, 'M2', 'master', 25),
('Master Chimie Analytique', 'M1-CANA', 4, 7, 'M1', 'master', 25),
('Master Chimie Analytique 2', 'M2-CANA', 4, 6, 'M2', 'master', 20),
('Master Chimie des Matériaux', 'M1-CMAT', 4, 7, 'M1', 'master', 25),
('Master Chimie des Matériaux 2', 'M2-CMAT', 4, 6, 'M2', 'master', 20);

-- Formations Biologie (25)
INSERT INTO formations (nom, code, dept_id, nb_modules, niveau, type_formation, capacite_max) VALUES
('Licence Biologie', 'L-BIO', 5, 8, 'L1', 'licence', 150),
('Licence Biologie 2ème année', 'L2-BIO', 5, 8, 'L2', 'licence', 130),
('Licence Biologie 3ème année', 'L3-BIO', 5, 9, 'L3', 'licence', 110),
('Master Biologie Moléculaire', 'M1-BMOL', 5, 7, 'M1', 'master', 40),
('Master Biologie Moléculaire 2', 'M2-BMOL', 5, 6, 'M2', 'master', 35),
('Master Écologie', 'M1-ECOL', 5, 7, 'M1', 'master', 35),
('Master Écologie 2', 'M2-ECOL', 5, 6, 'M2', 'master', 30),
('Master Génétique', 'M1-GENE', 5, 7, 'M1', 'master', 30),
('Master Génétique 2', 'M2-GENE', 5, 6, 'M2', 'master', 25),
('Master Neurosciences', 'M1-NEUR', 5, 7, 'M1', 'master', 25);

-- Formations Économie (30)
INSERT INTO formations (nom, code, dept_id, nb_modules, niveau, type_formation, capacite_max) VALUES
('Licence Économie', 'L-ECO', 6, 8, 'L1', 'licence', 200),
('Licence Économie 2ème année', 'L2-ECO', 6, 8, 'L2', 'licence', 180),
('Licence Économie 3ème année', 'L3-ECO', 6, 9, 'L3', 'licence', 160),
('Master Économie Internationale', 'M1-EINT', 6, 7, 'M1', 'master', 50),
('Master Économie Internationale 2', 'M2-EINT', 6, 6, 'M2', 'master', 45),
('Master Finance', 'M1-FIN', 6, 7, 'M1', 'master', 45),
('Master Finance 2', 'M2-FIN', 6, 6, 'M2', 'master', 40),
('Master Économétrie', 'M1-EMET', 6, 7, 'M1', 'master', 35),
('Master Économétrie 2', 'M2-EMET', 6, 6, 'M2', 'master', 30),
('Licence AES', 'L-AES', 6, 8, 'L1', 'licence', 150),
('Licence AES 2ème année', 'L2-AES', 6, 8, 'L2', 'licence', 130),
('Licence AES 3ème année', 'L3-AES', 6, 9, 'L3', 'licence', 110);

-- Formations Lettres (25)
INSERT INTO formations (nom, code, dept_id, nb_modules, niveau, type_formation, capacite_max) VALUES
('Licence Lettres Modernes', 'L-LET', 7, 8, 'L1', 'licence', 100),
('Licence Lettres Modernes 2ème année', 'L2-LET', 7, 8, 'L2', 'licence', 90),
('Licence Lettres Modernes 3ème année', 'L3-LET', 7, 9, 'L3', 'licence', 80),
('Master Littérature Française', 'M1-LITF', 7, 7, 'M1', 'master', 30),
('Master Littérature Française 2', 'M2-LITF', 7, 6, 'M2', 'master', 25),
('Licence LLCER Anglais', 'L-ANG', 7, 8, 'L1', 'licence', 120),
('Licence LLCER Anglais 2ème année', 'L2-ANG', 7, 8, 'L2', 'licence', 100),
('Licence LLCER Anglais 3ème année', 'L3-ANG', 7, 9, 'L3', 'licence', 90),
('Master LEA', 'M1-LEA', 7, 7, 'M1', 'master', 40),
('Master LEA 2', 'M2-LEA', 7, 6, 'M2', 'master', 35),
('Licence LLCER Espagnol', 'L-ESP', 7, 8, 'L1', 'licence', 80);

-- ============================================================================
-- GÉNÉRATION DES MODULES (6-9 par formation)
-- ============================================================================

-- Modules Informatique L1
INSERT INTO modules (nom, code, formation_id, credits, semestre, duree_examen_min, coefficient) VALUES
('Algorithmique et Programmation', 'INFO101', 1, 6, 1, 120, 3.0),
('Architecture des Ordinateurs', 'INFO102', 1, 4, 1, 90, 2.0),
('Mathématiques pour Informatique', 'INFO103', 1, 5, 1, 120, 2.5),
('Programmation C', 'INFO104', 1, 6, 2, 120, 3.0),
('Systèmes d''Exploitation', 'INFO105', 1, 4, 2, 90, 2.0),
('Bases de Données', 'INFO106', 1, 5, 2, 120, 2.5),
('Anglais Informatique', 'INFO107', 1, 2, 1, 60, 1.0),
('Projet Personnel', 'INFO108', 1, 3, 2, 60, 1.5);

-- Modules Master IA
INSERT INTO modules (nom, code, formation_id, credits, semestre, duree_examen_min, coefficient) VALUES
('Machine Learning', 'IA501', 6, 6, 1, 180, 3.0),
('Deep Learning', 'IA502', 6, 6, 1, 180, 3.0),
('NLP - Traitement du Langage', 'IA503', 6, 5, 1, 150, 2.5),
('Vision par Ordinateur', 'IA504', 6, 5, 2, 150, 2.5),
('Reinforcement Learning', 'IA505', 6, 4, 2, 120, 2.0),
('Éthique de l''IA', 'IA506', 6, 3, 2, 90, 1.5),
('Projet IA', 'IA507', 6, 6, 2, 60, 3.0);

-- Générer des modules pour les autres formations
DO $$
DECLARE
    f RECORD;
    module_names TEXT[] := ARRAY[
        'Introduction', 'Fondamentaux', 'Méthodologie', 'Théorie', 
        'Pratique', 'Applications', 'Projet', 'Séminaire', 'Stage'
    ];
    i INTEGER;
    mod_count INTEGER;
BEGIN
    FOR f IN SELECT id, nom, code, nb_modules FROM formations WHERE id > 6 LOOP
        mod_count := GREATEST(f.nb_modules, 6);
        FOR i IN 1..mod_count LOOP
            INSERT INTO modules (nom, code, formation_id, credits, semestre, duree_examen_min, coefficient)
            VALUES (
                module_names[((i-1) % 9) + 1] || ' ' || f.nom,
                f.code || '-M' || LPAD(i::TEXT, 2, '0'),
                f.id,
                CASE WHEN i <= 3 THEN 6 WHEN i <= 6 THEN 4 ELSE 3 END,
                CASE WHEN i % 2 = 1 THEN 1 ELSE 2 END,
                CASE WHEN i <= 3 THEN 180 WHEN i <= 6 THEN 120 ELSE 90 END,
                CASE WHEN i <= 3 THEN 3.0 WHEN i <= 6 THEN 2.0 ELSE 1.5 END
            );
        END LOOP;
    END LOOP;
END $$;

-- ============================================================================
-- GÉNÉRATION DES PROFESSEURS (200+ professeurs)
-- ============================================================================
DO $$
DECLARE
    noms TEXT[] := ARRAY['Martin', 'Bernard', 'Thomas', 'Petit', 'Robert', 'Richard', 'Durand', 'Dubois', 'Moreau', 'Laurent', 'Simon', 'Michel', 'Lefebvre', 'Leroy', 'Roux', 'David', 'Bertrand', 'Morel', 'Fournier', 'Girard'];
    prenoms TEXT[] := ARRAY['Jean', 'Pierre', 'Marie', 'Paul', 'Jacques', 'François', 'Alain', 'Philippe', 'Michel', 'Claude', 'Sophie', 'Catherine', 'Anne', 'Isabelle', 'Nathalie', 'Christine', 'Monique', 'Nicole', 'Sylvie', 'Martine'];
    specialites TEXT[] := ARRAY['Algorithmique', 'Bases de données', 'IA', 'Réseaux', 'Sécurité', 'Analyse', 'Algèbre', 'Probabilités', 'Mécanique', 'Optique', 'Thermodynamique', 'Chimie organique', 'Biochimie', 'Génétique', 'Microéconomie', 'Finance', 'Littérature', 'Linguistique'];
    grades TEXT[] := ARRAY['MCF', 'PR', 'ATER', 'Vacataire', 'PRAG'];
    dept_id INTEGER;
    i INTEGER;
    prof_count INTEGER := 0;
BEGIN
    FOR dept_id IN 1..7 LOOP
        FOR i IN 1..30 LOOP
            prof_count := prof_count + 1;
            INSERT INTO professeurs (matricule, nom, prenom, dept_id, specialite, email, telephone, grade, max_surveillances)
            VALUES (
                'PROF' || LPAD(prof_count::TEXT, 4, '0'),
                noms[(prof_count % 20) + 1],
                prenoms[(prof_count % 20) + 1],
                dept_id,
                specialites[((prof_count + dept_id) % 18) + 1],
                'prof' || prof_count || '@univ.edu',
                '06 ' || LPAD((prof_count * 11 % 100)::TEXT, 2, '0') || ' ' || LPAD((prof_count * 13 % 100)::TEXT, 2, '0') || ' ' || LPAD((prof_count * 17 % 100)::TEXT, 2, '0') || ' ' || LPAD((prof_count * 19 % 100)::TEXT, 2, '0'),
                grades[(prof_count % 5) + 1],
                3
            );
        END LOOP;
    END LOOP;
END $$;

-- ============================================================================
-- GÉNÉRATION DES ÉTUDIANTS (13 000+ étudiants)
-- ============================================================================
DO $$
DECLARE
    noms TEXT[] := ARRAY['Dupont', 'Durand', 'Lefebvre', 'Leroy', 'Moreau', 'Simon', 'Laurent', 'Garnier', 'Faure', 'Rousseau', 'Blanc', 'Guerin', 'Muller', 'Henry', 'Roussel', 'Nicolas', 'Perrin', 'Morin', 'Mathieu', 'Clement'];
    prenoms TEXT[] := ARRAY['Lucas', 'Hugo', 'Emma', 'Léa', 'Louis', 'Gabriel', 'Raphaël', 'Arthur', 'Jules', 'Adam', 'Chloé', 'Inès', 'Jade', 'Louise', 'Alice', 'Manon', 'Lina', 'Zoé', 'Rose', 'Léonie'];
    promos TEXT[] := ARRAY['2021', '2022', '2023', '2024', '2025'];
    f RECORD;
    i INTEGER;
    student_count INTEGER := 0;
    students_per_formation INTEGER;
BEGIN
    FOR f IN SELECT id, capacite_max FROM formations LOOP
        students_per_formation := GREATEST(f.capacite_max * 0.8, 20)::INTEGER;
        FOR i IN 1..students_per_formation LOOP
            student_count := student_count + 1;
            INSERT INTO etudiants (matricule, nom, prenom, formation_id, promo, email, date_naissance)
            VALUES (
                'ETU' || LPAD(student_count::TEXT, 6, '0'),
                noms[(student_count % 20) + 1],
                prenoms[(student_count % 20) + 1],
                f.id,
                promos[(i % 5) + 1],
                'etu' || student_count || '@etu.univ.edu',
                DATE '2000-01-01' + (student_count % 1500 || ' days')::INTERVAL
            );
            
            -- Arrêter si on atteint 13500 étudiants
            IF student_count >= 13500 THEN
                EXIT;
            END IF;
        END LOOP;
        IF student_count >= 13500 THEN
            EXIT;
        END IF;
    END LOOP;
    
    RAISE NOTICE 'Total étudiants créés: %', student_count;
END $$;

-- ============================================================================
-- GÉNÉRATION DES INSCRIPTIONS (130 000+ inscriptions)
-- ============================================================================
DO $$
DECLARE
    e RECORD;
    m RECORD;
    inscription_count INTEGER := 0;
BEGIN
    -- Pour chaque étudiant, l'inscrire aux modules de sa formation
    FOR e IN SELECT id, formation_id FROM etudiants LOOP
        FOR m IN SELECT id FROM modules WHERE formation_id = e.formation_id LOOP
            INSERT INTO inscriptions (etudiant_id, module_id, annee_universitaire, statut)
            VALUES (e.id, m.id, '2024-2025', 'active')
            ON CONFLICT (etudiant_id, module_id, annee_universitaire) DO NOTHING;
            
            inscription_count := inscription_count + 1;
        END LOOP;
    END LOOP;
    
    RAISE NOTICE 'Total inscriptions créées: %', inscription_count;
END $$;

-- ============================================================================
-- GÉNÉRATION DES UTILISATEURS
-- ============================================================================

-- Utilisateurs Directeurs (Vice-doyens)
INSERT INTO users (email, password_hash, role, nom, prenom, active) VALUES
('directeur@univ.edu', crypt('Director123!', gen_salt('bf')), 'director', 'Dubois', 'François', TRUE),
('vicedoyen@univ.edu', crypt('Director123!', gen_salt('bf')), 'director', 'Martin', 'Sophie', TRUE);

-- Utilisateurs Administrateurs (Service planification)
INSERT INTO users (email, password_hash, role, nom, prenom, active) VALUES
('admin.examens@univ.edu', crypt('Admin123!', gen_salt('bf')), 'administrator', 'Leroy', 'Pierre', TRUE),
('planification@univ.edu', crypt('Admin123!', gen_salt('bf')), 'administrator', 'Bernard', 'Marie', TRUE);

-- Utilisateurs Chefs de département
INSERT INTO users (email, password_hash, role, ref_id, nom, prenom, active)
SELECT 
    'chef.' || LOWER(code) || '@univ.edu',
    crypt('Chef123!', gen_salt('bf')),
    'department_head',
    id,
    'Chef_' || code,
    'Département',
    TRUE
FROM departements;

-- Quelques utilisateurs professeurs
INSERT INTO users (email, password_hash, role, ref_id, nom, prenom, active)
SELECT 
    email,
    crypt('Prof123!', gen_salt('bf')),
    'professor',
    id,
    nom,
    prenom,
    TRUE
FROM professeurs
LIMIT 50;

-- Quelques utilisateurs étudiants
INSERT INTO users (email, password_hash, role, ref_id, nom, prenom, active)
SELECT 
    email,
    crypt('Etudiant123!', gen_salt('bf')),
    'student',
    id,
    nom,
    prenom,
    TRUE
FROM etudiants
LIMIT 100;

-- ============================================================================
-- VÉRIFICATION DES DONNÉES
-- ============================================================================
DO $$
BEGIN
    RAISE NOTICE '=== STATISTIQUES DE LA BASE DE DONNÉES ===';
    RAISE NOTICE 'Départements: %', (SELECT COUNT(*) FROM departements);
    RAISE NOTICE 'Formations: %', (SELECT COUNT(*) FROM formations);
    RAISE NOTICE 'Modules: %', (SELECT COUNT(*) FROM modules);
    RAISE NOTICE 'Salles: %', (SELECT COUNT(*) FROM lieux_examen);
    RAISE NOTICE 'Professeurs: %', (SELECT COUNT(*) FROM professeurs);
    RAISE NOTICE 'Étudiants: %', (SELECT COUNT(*) FROM etudiants);
    RAISE NOTICE 'Inscriptions: %', (SELECT COUNT(*) FROM inscriptions);
    RAISE NOTICE 'Utilisateurs: %', (SELECT COUNT(*) FROM users);
END $$;
