import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "survival.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_lung_dataframe() -> pd.DataFrame:
    
    query = """
        SELECT p.patient_id, p.age, p.sex, p.ph_ecog AS "ph.ecog",
               p.wt_loss AS "wt.loss", f.time_days AS time, f.status
        FROM patients p
        JOIN follow_up f ON p.patient_id = f.patient_id
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df