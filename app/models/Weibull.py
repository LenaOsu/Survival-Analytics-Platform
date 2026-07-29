from os import name

from lifelines.datasets import load_dd, load_waltons, load_lung
from lifelines import KaplanMeierFitter, WeibullFitter
from lifelines.utils import median_survival_times
from lifelines.statistics import logrank_test
import pandas as pd                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
from lifelines import *
from lifelines import CoxPHFitter
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from lifelines.utils import concordance_index

def democracy_Wb():

    data = load_dd()
    df = pd.DataFrame(data)

    T = data["duration"] # power in place
    E = data["observed"] # end of the power in place ~ death/exit

    wbf_democracy = WeibullFitter()
    wbf_ndemocracy = WeibullFitter()

    dem = (data["democracy"] == "Democracy")

    wbf_democracy.fit(T[dem], event_observed=E[dem], label = "Democratic Regime")

    med_dem_w = wbf_democracy.median_survival_time_
    med_dem_conf_w = median_survival_times(wbf_democracy.confidence_interval_)

    wbf_ndemocracy.fit(T[~dem], event_observed=E[~dem], label = "Non Democratic Regime")

    med_ndem_w = wbf_ndemocracy.median_survival_time_
    med_ndem_conf_w = median_survival_times(wbf_ndemocracy.confidence_interval_)
    results_w = logrank_test(T[dem], T[~dem], E[dem], E[~dem], alpha=.99)

    return wbf_democracy, wbf_ndemocracy, df, dem, T, E, med_dem_w, med_dem_conf_w, med_ndem_w, med_ndem_conf_w, results_w

def Wb_lung():

    data_lung = load_lung()
    df_lung = pd.DataFrame(data_lung)
    #print(df_lung.columns)
    #print(df_lung.head())

    print(df_lung["status"].value_counts())

    # Cox veut un DataFrame avec : les covariables + une colonne temps + une colonne evenement
    df_cox = df_lung[["time", "status", "age", "sex", "ph.ecog", "wt.loss"]].dropna()
    df_cox["event"] = (df_cox["status"] == 1).astype(int)  # verifie le codage exact de status dans load_lung
    df_cox = df_cox.drop(columns="status")

    print(df_cox["status"].value_counts() if "status" in df_cox.columns else "colonne status deja supprimee")


    df_train, df_test = train_test_split(df_cox, test_size=0.2, random_state=42)
    print(df_train.nunique())
    print(df_train.describe())
    scores = {}
 
    T = data_lung["time"] #observation time
    E = (data_lung["status"] == 1).astype(int) #death or censured (not dead yet or exit)
    wbf_lung_m = WeibullFitter()
    wbf_lung_w = WeibullFitter()

    sexe = (data_lung["sex"] == 1)

    cph = CoxPHFitter()
    cph.fit(df_train, duration_col="time", event_col="event")
    cph.print_summary()  # coefficients, hazard ratios, p-values par covariable
    risk_train = cph.predict_partial_hazard(df_train)
    risk_test = cph.predict_partial_hazard(df_test)

    c_index_train = concordance_index(
    df_train["time"], -risk_train, df_train["event"]
    )
    c_index_test = concordance_index(
        df_test["time"], -risk_test, df_test["event"]
    )

    gap = c_index_train - c_index_test

    print(f"C-index train={c_index_train:.3f} | C-index test={c_index_test:.3f} | gap={gap:.3f}")

    if c_index_train < 0.6 and c_index_test < 0.6:
        diagnostic = "SOUS-APPRENTISSAGE (le modele ordonne mal les patients, meme sur train)"
    elif gap > 0.1:
        diagnostic = "SUR-APPRENTISSAGE (gros ecart train/test)"
    else:
        diagnostic = "OK"

    print(f"-> {diagnostic}")

    wbf_lung_m.fit(T[sexe], event_observed = E[sexe], label = "Men lung disease")
    med_men_wb = wbf_lung_m.median_survival_time_
    med_men_conf_wb = median_survival_times(wbf_lung_m.confidence_interval_)



    wbf_lung_w.fit(T[~sexe], event_observed = E[~sexe], label = "Women lung disease")
    med_women_wb = wbf_lung_w.median_survival_time_
    med_women_conf_wb = median_survival_times(wbf_lung_w.confidence_interval_)


    results_lung_wb = logrank_test(T[sexe], T[~sexe], E[sexe], E[~sexe], alpha=.99)

    return wbf_lung_m, wbf_lung_w, df_lung, T, E, sexe, med_men_wb, med_men_conf_wb, med_women_wb, med_women_conf_wb, results_lung_wb