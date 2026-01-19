-- ============================================================================
-- REQUÊTES AVANCÉES POUR LE DASHBOARD
-- Plateforme d'Optimisation des EDT d'Examens Universitaires
-- ============================================================================

-- ============================================================================
-- 1. STATISTIQUES GLOBALES
-- ============================================================================

-- Nombre total d'entités
SELECT 
    (SELECT COUNT(*) FROM departements) as nb_departements,
    (SELECT COUNT(*) FROM formations) as nb_formations,
    (SELECT COUNT(*) FROM modules) as nb_modules,
    (SELECT COUNT(*) FROM professeurs) as nb_professeurs,
    (SELECT COUNT(*) FROM etudiants) as nb_etudiants,
    (SELECT COUNT(*) FROM inscriptions) as nb_inscriptions,
    (SELECT COUNT(*) FROM lieux_examen) as nb_salles,
    (SELECT COUNT(*) FROM examens WHERE statut NOT IN ('cancelled', 'draft')) as nb_examens_planifies;

-- ============================================================================
-- 2. KPIs PAR DÉPARTEMENT
-- ============================================================================

SELECT 
    d.id,
    d.nom,
    d.code,
    COUNT(DISTINCT f.id) as nb_formations,
    COUNT(DISTINCT m.id) as nb_modules,
    COUNT(DISTINCT p.id) as nb_professeurs,
    COUNT(DISTINCT et.id) as nb_etudiants,
    COUNT(DISTINCT e.id) as nb_examens_planifies,
    ROUND(
        100.0 * COUNT(DISTINCT e.id) / NULLIF(COUNT(DISTINCT m.id), 0), 
        2
    ) as taux_planification
FROM departements d
LEFT JOIN formations f ON f.dept_id = d.id
LEFT JOIN modules m ON m.formation_id = f.id
LEFT JOIN professeurs p ON p.dept_id = d.id
LEFT JOIN etudiants et ON et.formation_id = f.id
LEFT JOIN examens e ON e.module_id = m.id AND e.statut NOT IN ('cancelled', 'draft')
GROUP BY d.id, d.nom, d.code
ORDER BY d.nom;

-- ============================================================================
-- 3. OCCUPATION DES SALLES
-- ============================================================================

SELECT 
    l.id,
    l.nom,
    l.code,
    l.capacite,
    l.capacite / 2 as capacite_examen,
    l.type,
    l.batiment,
    COUNT(e.id) as nb_examens,
    COALESCE(SUM(e.nb_inscrits), 0) as total_etudiants,
    ROUND(
        100.0 * COUNT(e.id) / 
        NULLIF((SELECT COUNT(*) FROM examens WHERE statut NOT IN ('cancelled', 'draft')), 0),
        2
    ) as part_examens_pct
FROM lieux_examen l
LEFT JOIN examens e ON e.salle_id = l.id AND e.statut NOT IN ('cancelled', 'draft')
GROUP BY l.id, l.nom, l.code, l.capacite, l.type, l.batiment
ORDER BY nb_examens DESC;

-- ============================================================================
-- 4. DÉTECTION DES CONFLITS
-- ============================================================================

-- Conflits de chevauchement de salles
SELECT 
    e1.id as examen1_id,
    e2.id as examen2_id,
    l.nom as salle,
    e1.date_heure as debut1,
    e1.date_heure + (e1.duree_minutes || ' minutes')::INTERVAL as fin1,
    e2.date_heure as debut2,
    e2.date_heure + (e2.duree_minutes || ' minutes')::INTERVAL as fin2,
    'CONFLIT SALLE' as type_conflit
FROM examens e1
JOIN examens e2 ON e1.salle_id = e2.salle_id 
    AND e1.id < e2.id
    AND e1.statut NOT IN ('cancelled', 'draft')
    AND e2.statut NOT IN ('cancelled', 'draft')
JOIN lieux_examen l ON l.id = e1.salle_id
WHERE (e1.date_heure, e1.date_heure + (e1.duree_minutes || ' minutes')::INTERVAL)
    OVERLAPS (e2.date_heure, e2.date_heure + (e2.duree_minutes || ' minutes')::INTERVAL);

-- Professeurs surchargés (plus de 3 examens par jour)
SELECT 
    p.id,
    p.nom,
    p.prenom,
    DATE(e.date_heure) as jour,
    COUNT(*) as nb_examens,
    'SURCHARGE PROFESSEUR' as type_conflit
FROM examens e
JOIN professeurs p ON p.id = e.prof_id
WHERE e.statut NOT IN ('cancelled', 'draft')
GROUP BY p.id, p.nom, p.prenom, DATE(e.date_heure)
HAVING COUNT(*) > 3
ORDER BY jour, nb_examens DESC;

-- ============================================================================
-- 5. PLANNING PAR FORMATION
-- ============================================================================

SELECT 
    f.nom as formation,
    f.niveau,
    d.nom as departement,
    m.nom as module,
    e.date_heure,
    e.duree_minutes,
    l.nom as salle,
    l.batiment,
    CONCAT(p.prenom, ' ', p.nom) as surveillant,
    e.nb_inscrits,
    e.statut
FROM examens e
JOIN modules m ON m.id = e.module_id
JOIN formations f ON f.id = m.formation_id
JOIN departements d ON d.id = f.dept_id
LEFT JOIN lieux_examen l ON l.id = e.salle_id
LEFT JOIN professeurs p ON p.id = e.prof_id
WHERE e.statut NOT IN ('cancelled')
ORDER BY f.nom, e.date_heure;

-- ============================================================================
-- 6. RÉPARTITION DES SURVEILLANCES
-- ============================================================================

SELECT 
    p.id,
    p.matricule,
    CONCAT(p.prenom, ' ', p.nom) as nom_complet,
    d.nom as departement,
    COUNT(e.id) as nb_surveillances,
    p.max_surveillances * 
        (SELECT COUNT(DISTINCT DATE(date_heure)) FROM examens WHERE statut NOT IN ('cancelled', 'draft')) 
        as max_possible,
    ROUND(
        100.0 * COUNT(e.id) / NULLIF(
            p.max_surveillances * 
            (SELECT COUNT(DISTINCT DATE(date_heure)) FROM examens WHERE statut NOT IN ('cancelled', 'draft')),
            0
        ),
        2
    ) as taux_charge_pct
FROM professeurs p
JOIN departements d ON d.id = p.dept_id
LEFT JOIN examens e ON e.prof_id = p.id AND e.statut NOT IN ('cancelled', 'draft')
GROUP BY p.id, p.matricule, p.prenom, p.nom, d.nom, p.max_surveillances
ORDER BY nb_surveillances DESC;

-- ============================================================================
-- 7. EXAMENS PAR CRÉNEAU HORAIRE
-- ============================================================================

SELECT 
    DATE(e.date_heure) as jour,
    EXTRACT(HOUR FROM e.date_heure) as heure,
    COUNT(*) as nb_examens,
    SUM(e.nb_inscrits) as total_etudiants,
    COUNT(DISTINCT e.salle_id) as salles_utilisees
FROM examens e
WHERE e.statut NOT IN ('cancelled', 'draft')
GROUP BY DATE(e.date_heure), EXTRACT(HOUR FROM e.date_heure)
ORDER BY jour, heure;

-- ============================================================================
-- 8. CAPACITÉ VS INSCRITS
-- ============================================================================

SELECT 
    e.id as examen_id,
    m.nom as module,
    l.nom as salle,
    l.capacite / 2 as capacite_examen,
    e.nb_inscrits,
    CASE 
        WHEN e.nb_inscrits > l.capacite / 2 THEN 'DÉPASSEMENT'
        WHEN e.nb_inscrits > l.capacite / 2 * 0.9 THEN 'PROCHE LIMITE'
        ELSE 'OK'
    END as statut_capacite,
    e.nb_inscrits - (l.capacite / 2) as difference
FROM examens e
JOIN modules m ON m.id = e.module_id
JOIN lieux_examen l ON l.id = e.salle_id
WHERE e.statut NOT IN ('cancelled', 'draft')
ORDER BY difference DESC;

-- ============================================================================
-- 9. SESSIONS DE GÉNÉRATION
-- ============================================================================

SELECT 
    s.id,
    u.email as utilisateur,
    s.date_debut,
    s.date_fin,
    s.statut,
    s.nb_examens_planifies,
    s.nb_conflits_resolus,
    s.temps_execution_ms,
    s.parametres
FROM sessions_generation s
JOIN users u ON u.id = s.user_id
ORDER BY s.date_debut DESC
LIMIT 10;

-- ============================================================================
-- 10. VÉRIFICATION INTÉGRITÉ DONNÉES
-- ============================================================================

-- Modules sans examen planifié
SELECT 
    m.id,
    m.nom,
    m.code,
    f.nom as formation,
    (SELECT COUNT(*) FROM inscriptions WHERE module_id = m.id AND statut = 'active') as nb_inscrits
FROM modules m
JOIN formations f ON f.id = m.formation_id
WHERE NOT EXISTS (
    SELECT 1 FROM examens e WHERE e.module_id = m.id AND e.statut NOT IN ('cancelled', 'draft')
)
AND EXISTS (
    SELECT 1 FROM inscriptions i WHERE i.module_id = m.id AND i.statut = 'active'
)
ORDER BY nb_inscrits DESC;

-- Examens sans surveillant assigné
SELECT 
    e.id,
    m.nom as module,
    e.date_heure,
    l.nom as salle,
    e.nb_inscrits
FROM examens e
JOIN modules m ON m.id = e.module_id
LEFT JOIN lieux_examen l ON l.id = e.salle_id
WHERE e.prof_id IS NULL
AND e.statut NOT IN ('cancelled', 'draft')
ORDER BY e.date_heure;
