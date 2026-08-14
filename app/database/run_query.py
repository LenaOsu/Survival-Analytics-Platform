# app/database/run_query.py
from pathlib import Path
import pandas as pd
from app.database.repository import get_connection

QUERIES_DIR = Path(__file__).parent / "queries"
OUTPUT_DIR = Path(__file__).parent / "outputs"

def run_query_file(filename: str) -> pd.DataFrame:
    query = (QUERIES_DIR / filename).read_text()
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def export_query_to_csv(filename: str) -> Path:
    df = run_query_file(filename)
    OUTPUT_DIR.mkdir(exist_ok=True)

    output_name = filename.replace(".sql", ".csv")
    output_path = OUTPUT_DIR / output_name

    df.to_csv(output_path, index=False)
    print(f"{filename} -> {output_path} ({len(df)} lignes)")
    return output_path

if __name__ == "__main__":
    query_files = [
        "cohort_stat.sql",
        "age_ecog_cross.sql",
        "risk_ranking_overview.sql",
        "death_ecog_status.sql",
    ]

    for filename in query_files:
        export_query_to_csv(filename)