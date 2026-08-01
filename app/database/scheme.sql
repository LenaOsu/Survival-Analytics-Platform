CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY,
    age INTEGER,
    sex INTEGER CHECK(sex IN (1, 2)), 
    ph_ecog INTEGER,
    wt_loss REAL
);

CREATE TABLE IF NOT EXISTS follow_up (
    patient_id INTEGER PRIMARY KEY REFERENCES patients(patient_id),
    time_days INTEGER NOT NULL,
    status INTEGER CHECK(status IN (0, 1)) 
);