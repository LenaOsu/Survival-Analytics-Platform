from app.database.repository import get_lung_dataframe
import pandas as pd


def load_survival_data():

    data_lung = get_lung_dataframe()
    df_lung = pd.DataFrame(data_lung)

    T = data_lung["time"]  # observation time
    E = (data_lung["status"] == 1).astype(int)  # 1 = death, 0 = censored

    # sex coding confirmed against the source dataset documentation
    # (R package survival::lung --> reused as-is by lifelines): 1 = male, 2 = female
    sexe = (data_lung["sex"] == 1)  # True = men

    return df_lung, T, E, sexe