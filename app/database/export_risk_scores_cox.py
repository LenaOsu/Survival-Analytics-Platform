from app.database.repository import get_connection, get_lung_dataframe
from lifelines import CoxPHFitter

def export_risk_scores_cox():
    # Get the lung dataframe from the database
    conn = get_connection()
    df = get_lung_dataframe()

    # Prepare the data for Cox model
    df_cox = df[["patient_id", "time", "status", "age", "sex", "ph.ecog", "wt.loss"]].dropna()
    df_cox["event"] = (df_cox["status"] == 1).astype(int)
    fit_df = df_cox.drop(columns=["status", "patient_id"]) #on drop patient id pour le fit, mais on le garde pour l'export des scores + status pour ne pas avoir deux fois la meme colonne

    cph = CoxPHFitter()
    cph.fit(fit_df, duration_col="time", event_col="event")

    # Predict risk scores for all patients
    df_cox["partial_hazard"] = cph.predict_partial_hazard(fit_df)
    
