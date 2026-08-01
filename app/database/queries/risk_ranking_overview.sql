SELECT p.patient_id, p.age, p.sex, p.ph_ecog, p.wt_loss, f.status, f.time_days,
RANK () OVER (
    PARTITION BY CASE WHEN p.age < 50 THEN 'less than 50 years' ELSE 'bit older' END
    ORDER BY p.wt_loss DESC, f.time_days ASC
) AS rank_weight_loss_time,
NTILE(4) OVER (ORDER BY p.wt_loss DESC) AS quartile_risque
FROM patients p
JOIN follow_up f ON p.patient_id = f.patient_id
WHERE p.age IS NOT NULL AND p.wt_loss IS NOT NULL
ORDER BY quartile_risque, rank_weight_loss_time