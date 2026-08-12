SELECT p.patient_id, p.ph_ecog, p.wt_loss, f.status, 
FROM patients p
JOIN follow_up f ON p.patient_id = f.patient_id
WHERE p.ph_ecog > 3 AND p.wt_loss > 10
GROUP BY p.patient_id


