import sqlite3
from pathlib import Path
from lifelines.datasets import load_lung

DB_PATH = Path(__file__).parent / "survival.db"
SCHEMA_PATH = Path(__file__).parent / "scheme.sql"

def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text())

    data = load_lung().reset_index().rename(columns={"index": "patient_id"})

    patients = data[["patient_id", "age", "sex", "ph.ecog", "wt.loss"]].rename(
        columns={"ph.ecog": "ph_ecog", "wt.loss": "wt_loss"}
    )
    follow_up = data[["patient_id", "time", "status"]].rename(
        columns={"time": "time_days"}
    )

    patients.to_sql("patients", conn, if_exists="replace", index=False)
    follow_up.to_sql("follow_up", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print(f"Base peuplee : {DB_PATH}")

if __name__ == "__main__":
    seed()