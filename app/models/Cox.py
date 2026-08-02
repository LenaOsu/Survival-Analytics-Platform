from os import name

from app.database.repository import get_lung_dataframe
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


def Cox_lung():

    data_lung = get_lung_dataframe()
    df_lung = pd.DataFrame(data_lung)

    print(df_lung["status"].value_counts())
    print(df_lung["sex"].value_counts())

    df_cox = df_lung[["time", "status", "age", "sex", "ph.ecog", "wt.loss"]].dropna()
    df_cox["event"] = (df_cox["status"] == 1).astype(int)
    df_cox = df_cox.drop(columns="status")

    df_train, df_test = train_test_split(df_cox, test_size=0.2, random_state=42)
    print(df_train.nunique())
    print(df_train.describe())

    # Cox 
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

    #Comparaison Cox vs Weibull, train vs test
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig1, axes1 = plt.subplots(1, 2, figsize=(12, 5))
    
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

    fig.tight_layout()
    fig.savefig("outputs/plots/cox_vs_wb.png", dpi=130)

    for ax, df_subset, label in zip(axes1, [df_train, df_test], ["Train", "Test"]):
    
        km_split = KaplanMeierFitter()
        km_split.fit(df_subset["time"], event_observed=df_subset["event"], label="Kaplan-Meier (ajuste sur ce split)")
        km_split.plot_survival_function(ax=ax, ci_show=True)
        
        surv_funcs = cph.predict_survival_function(df_subset)
        surv_funcs.mean(axis=1).plot(ax=ax, label="Cox (moyenne predite)", linestyle="--")

        ax.set_title(f"{label} : Cox vs Kaplan-Meier")
        ax.set_xlabel("Temps")
        ax.set_ylabel("Probabilite de survie")
        ax.legend()
        ax.grid(alpha=0.3)

    fig1.tight_layout()
    fig1.savefig("outputs/plots/cox_vs_km.png", dpi=130)
    

    plt.show()

