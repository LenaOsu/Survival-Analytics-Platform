/*SELECT p.patient_id, p.ph_ecog, p.wt_loss, f.status, f.time_days
FROM patients p
JOIN follow_up f ON p.patient_id = f.patient_id
WHERE p.ph_ecog >= 3 AND p.wt_loss > 10
ORDER BY f.status DESC, p.wt_loss DESC, f.time_days ASC*/

#########################################

SELECT p.patient_id, p.ph_ecog, f.status,
CASE 
WHEN p.ph_ecog = 0 THEN 'ECOG 0 No impact on daily living'
WHEN p.ph_ecog = 1 THEN 'ECOG 1 Mild impairment'
WHEN p.ph_ecog = 2 THEN 'ECOG 2 Moderate impairment'
WHEN p.ph_ecog = 3 THEN 'ECOG 3 Severe impairment'
WHEN p.ph_ecog = 4 THEN 'ECOG 4 Complete disability'
ELSE 'ECOG unknown'
END AS ph_ecog_group,
CASE
WHEN f.status = 1 THEN 'Death'
WHEN f.status = 0 THEN 'Censored'
END AS status_label
FROM patients p
JOIN follow_up f ON p.patient_id = f.patient_id
COUNT(*) AS n_patients,
SUM(f.status) AS n_deaths,
WHERE p.ph_ecog >= 3 
GROUP BY p.age
HAVING n_patients > 0
