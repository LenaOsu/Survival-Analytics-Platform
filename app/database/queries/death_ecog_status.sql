SELECT p.patient_id, p.ph_ecog, p.wt_loss, f.status, f.time_days
FROM patients p
JOIN follow_up f ON p.patient_id = f.patient_id
WHERE p.ph_ecog >= 3 AND p.wt_loss > 10
ORDER BY f.status DESC, p.wt_loss DESC, f.time_days ASC

