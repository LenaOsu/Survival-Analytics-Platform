from app.src.data_loader import load_survival_data
from lifelines import WeibullFitter
from lifelines.utils import median_survival_times
from lifelines.statistics import logrank_test
from lifelines import *



def Wb_lung():

    df_lung, T, E, sexe = load_survival_data()


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