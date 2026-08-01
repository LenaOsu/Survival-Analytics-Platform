from os import name

from lifelines.datasets import load_dd, load_waltons, load_lung
from lifelines import KaplanMeierFitter, WeibullFitter
from lifelines.utils import k_fold_cross_validation, median_survival_times
from lifelines.statistics import logrank_test
import pandas as pd                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
from lifelines import *
from lifelines import CoxPHFitter
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from lifelines.utils import concordance_index
from matplotlib import pyplot as plt


def Wb_lung():

    data_lung = load_lung()
    df_lung = pd.DataFrame(data_lung)

    print(df_lung["status"].value_counts())
    print(df_lung["sex"].value_counts())

    df_cox = df_lung[["time", "status", "age", "sex", "ph.ecog", "wt.loss"]].dropna()
    df_cox["event"] = (df_cox["status"] == 1).astype(int)
    df_cox = df_cox.drop(columns="status")

    df_train, df_test = train_test_split(df_cox, test_size=0.2, random_state=42)
    print(df_train.nunique())
    print(df_train.describe())

    T = data_lung["time"]
    E = (data_lung["status"] == 1).astype(int)
    sexe = (data_lung["sex"] == 1)

    # ---- Cox : creation, entrainement, evaluation (AVANT toute utilisation) ----
    cph = CoxPHFitter()
    cph.fit(df_train, duration_col="time", event_col="event")
    cph.print_summary()

    risk_train = cph.predict_partial_hazard(df_train)
    risk_test = cph.predict_partial_hazard(df_test)

    c_index_train = concordance_index(df_train["time"], -risk_train, df_train["event"])
    c_index_test = concordance_index(df_test["time"], -risk_test, df_test["event"])
    gap = c_index_train - c_index_test

    print(f"C-index train={c_index_train:.3f} | C-index test={c_index_test:.3f} | gap={gap:.3f}")

    if c_index_train < 0.6 and c_index_test < 0.6:
        diagnostic = "SOUS-APPRENTISSAGE (le modele ordonne mal les patients, meme sur train)"
    elif gap > 0.1:
        diagnostic = "SUR-APPRENTISSAGE (gros ecart train/test)"
    else:
        diagnostic = "OK"
    print(f"-> {diagnostic}")

    cv_scores = k_fold_cross_validation(
        cph, df_cox, duration_col="time", event_col="event",
        k=5, scoring_method="concordance_index"
    )
    print("CV C-index (5 folds):", cv_scores, "moyenne:", sum(cv_scores) / len(cv_scores))

    # ---- Comparaison visuelle Cox vs Weibull, train vs test ----
    # objet Weibull dedie a CETTE comparaison, distinct de wbf_lung_m/wbf_lung_w utilises plus bas
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, df_subset, label in zip(axes, [df_train, df_test], ["Train", "Test"]):
        wbf_split = WeibullFitter()
        wbf_split.fit(df_subset["time"], event_observed=df_subset["event"], label="Weibull (ajuste sur ce split)")
        wbf_split.plot_survival_function(ax=ax, ci_show=True)

        surv_funcs = cph.predict_survival_function(df_subset)
        surv_funcs.mean(axis=1).plot(ax=ax, label="Cox (moyenne predite)", linestyle="--")

        ax.set_title(f"{label} : Cox vs Weibull")
        ax.set_xlabel("Temps")
        ax.set_ylabel("Probabilite de survie")
        ax.legend()
        ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("outputs/plots/cox_vs_wb.png", dpi=130)
    plt.show()

    # ---- Weibull hommes vs femmes (comparaison clinique, independante du split train/test) ----
    wbf_lung_m = WeibullFitter()
    wbf_lung_w = WeibullFitter()

    wbf_lung_m.fit(T[sexe], event_observed=E[sexe], label="Men lung disease")
    med_men_wb = wbf_lung_m.median_survival_time_
    med_men_conf_wb = median_survival_times(wbf_lung_m.confidence_interval_)

    wbf_lung_w.fit(T[~sexe], event_observed=E[~sexe], label="Women lung disease")
    med_women_wb = wbf_lung_w.median_survival_time_
    med_women_conf_wb = median_survival_times(wbf_lung_w.confidence_interval_)

    results_lung_wb = logrank_test(T[sexe], T[~sexe], E[sexe], E[~sexe], alpha=.99)

    return wbf_lung_m, wbf_lung_w, df_lung, T, E, sexe, med_men_wb, med_men_conf_wb, med_women_wb, med_women_conf_wb, results_lung_wb