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


def Wb_lung():

    data_lung = get_lung_dataframe()
    df_lung = pd.DataFrame(data_lung)

    print(df_lung["status"].value_counts())
    print(df_lung["sex"].value_counts())


    T = data_lung["time"]
    E = (data_lung["status"] == 1).astype(int)
    sexe = (data_lung["sex"] == 1)


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