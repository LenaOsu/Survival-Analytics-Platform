from lifelines.datasets import load_dd, load_waltons, load_lung
from lifelines import KaplanMeierFitter, WeibullFitter
from lifelines.utils import median_survival_times
from lifelines.statistics import logrank_test
import pandas as pd
from lifelines import *
 

def death_risk(wbf_lung_w, wbf_lung_m):

    threshold = 365

    risk_w = 1 - wbf_lung_w.survival_function_at_times(threshold).iloc[0]
    risk_m = 1 - wbf_lung_m.survival_function_at_times(threshold).iloc[0]

    print(f"Risk of death before {threshold} days:")
    print(f"Women: {risk_w:.2%}")
    print(f"Men: {risk_m:.2%}")

def error_model(kmf_lung_w, wbf_lung_w, kmf_lung_m, wbf_lung_m):

    times = [180, 300, 500, 730]

    for t in times:
        km_w = kmf_lung_w.survival_function_at_times(t).iloc[0]
        wb_w = wbf_lung_w.survival_function_at_times(t).iloc[0]

        km_m = kmf_lung_m.survival_function_at_times(t).iloc[0]
        wb_m = wbf_lung_m.survival_function_at_times(t).iloc[0]

        print(f"Women t={t}: KM={km_w*100:.3f} | Weibull={wb_w*100:.3f} | diff={abs(km_w-wb_w)*100:.3f}")
        print(f"Men t={t}: KM={km_m*100:.3f} | Weibull={wb_m*100:.3f} | diff={abs(km_m-wb_m)*100:.3f}")

    return km_w, wb_w, km_m, wb_m

def horizon_probability(kmf_lung_w, kmf_lung_m):

    horizons = [180, 300, 500, 730]

    for t in horizons:
        print(
            f"t={t} days | Women KM={kmf_lung_w.predict(t):.2%} | Men KM={kmf_lung_m.predict(t):.2%}"
        )

def summary(med_women, med_women_wb, med_men, med_men_wb, wbf_lung_w, wbf_lung_m, kmf_lung_w, kmf_lung_m):

    print(f"--- WOMEN ---")
    print("KM median:", med_women)
    print("Weibull median:", med_women_wb)
    print("Weibull rho:", wbf_lung_w.rho_)
    print("Weibull lambda:", wbf_lung_w.lambda_)

    print(f"--- MEN ---")
    print("KM median:", med_men)
    print("Weibull median:", med_men_wb)
    print("Weibull rho:", wbf_lung_m.rho_)
    print("Weibull lambda:", wbf_lung_m.lambda_)




