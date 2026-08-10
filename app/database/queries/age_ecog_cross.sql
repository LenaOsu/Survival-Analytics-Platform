SELECT
CASE 
p.sex WHEN 1 THEN 'Men' WHEN 2 THEN 'Women' END AS sex,
CASE 
WHEN p.age < 50 THEN 'age<50 years'
WHEN p.age >= 50 AND p.age < 60 THEN 'age 50-59 years'
WHEN p.age >= 60 AND p.age < 70 THEN 'age 60-69 years'
WHEN p.age >= 70 AND p.age < 80 THEN 'age 70-79 years'
WHEN p.age >= 80 THEN 'age>=80 years'
END AS age_group,
CASE 
WHEN p.ph_ecog = 0 THEN 'ECOG 0 No impact on daily living'
WHEN p.ph_ecog = 1 THEN 'ECOG 1 Mild impairment'
WHEN p.ph_ecog = 2 THEN 'ECOG 2 Moderate impairment'
WHEN p.ph_ecog = 3 THEN 'ECOG 3 Severe impairment'
WHEN p.ph_ecog = 4 THEN 'ECOG 4 Complete disability'
ELSE 'ECOG unknown'
END AS ph_ecog_group,
COUNT(*) AS n_patients,
ROUND(AVG(f.time_days), 1) AS mean_followup_days,
SUM(f.status) AS n_deaths,
ROUND(100.0*SUM(f.status)/COUNT(*), 1) || '%' AS pct_deaths 
FROM patients p
JOIN follow_up f ON p.patient_id = f.patient_id
GROUP BY sex, age_group, ph_ecog_group
ORDER BY age_group, ph_ecog_group;