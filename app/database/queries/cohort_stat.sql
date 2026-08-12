SELECT 
CASE p.sex WHEN 1 THEN 'Men' WHEN 2 THEN 'Women' END AS sexe,
COUNT(*) AS n_patients,
SUM(f.status) AS n_deaths,
ROUND(100.0*SUM(f.status)/COUNT(*), 1) || '%' AS pct_deaths,
ROUND(AVG(f.time_days), 1) AS mean_followup_days,
ROUND(AVG(p.age), 1) AS mean_age
FROM patients p
JOIN follow_up f ON p.patient_id = f.patient_id
GROUP BY sexe

#pour les deux sexes homme/femme, on compte le nombre de patients, le nombre de décès, le pourcentage de décès, la durée moyenne de suivi et l'âge moyen.