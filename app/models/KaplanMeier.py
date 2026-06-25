from lifelines.datasets import load_dd, load_waltons, load_lung
from lifelines import KaplanMeierFitter, WeibullFitter
from lifelines.utils import median_survival_times
from lifelines.statistics import logrank_test
import pandas as pd
from lifelines import *


def democracy_KM():

    data = load_dd()
    T = data["duration"] # power in place
    E = data["observed"] # end of the power in place ~ death/exit

    df = pd.DataFrame(data)
    #print(df.head())
    #print(df.columns)

    kmf_democracy = KaplanMeierFitter()
    kmf_ndemocracy = KaplanMeierFitter()
    dem = (data["democracy"] == "Democracy")

    kmf_democracy.fit(T[dem], event_observed=E[dem], label = "Democratic Regime")

    med_dem = kmf_democracy.median_survival_time_
    med_dem_conf = median_survival_times(kmf_democracy.confidence_interval_)

    kmf_ndemocracy.fit(T[~dem], event_observed=E[~dem], label = "Non Democratic Regime")

    med_ndem = kmf_ndemocracy.median_survival_time_
    med_ndem_conf = median_survival_times(kmf_ndemocracy.confidence_interval_)

    results = logrank_test(T[dem], T[~dem], E[dem], E[~dem], alpha=.99)

    return kmf_democracy, kmf_ndemocracy, dem, T, E, med_dem, med_dem_conf, med_ndem, med_ndem_conf, results

def KM_lung():

    data_lung = load_lung()
    df_lung = pd.DataFrame(data_lung)
    #print(df_lung.columns)
    #print(df_lung.head())

    #status = 0 or 1; sex = 1 or 2- cannot know for sure who is who
    #have a look on df_lung.groupby("status")["time"].mean() and df.groupby("status")["time"]
    #ALWAYS check the documentation to be sure of the object

    T = data_lung["time"] #observation time
    #print("A")
    E = (data_lung["status"] == 1).astype(int) #death or censured (not dead yet or exit)
    #print("B")
    kmf_lung_m = KaplanMeierFitter()
    kmf_lung_w = KaplanMeierFitter()
    #print("C")

    sexe = (data_lung["sex"] == 1) #corresponds to men or women according the documentation

    kmf_lung_m.fit(T[sexe], event_observed = E[sexe], label = "Men lung disease")
    med_men = kmf_lung_m.median_survival_time_
    med_men_conf = median_survival_times(kmf_lung_m.confidence_interval_)

    kmf_lung_w.fit(T[~sexe], event_observed = E[~sexe], label = "Women lung disease")
    med_women = kmf_lung_w.median_survival_time_
    med_women_conf = median_survival_times(kmf_lung_w.confidence_interval_)

    results_lung = logrank_test(T[sexe], T[~sexe], E[sexe], E[~sexe], alpha=.99)

    return kmf_lung_m, kmf_lung_w, df_lung, T, E, sexe, med_men, med_men_conf, med_women, med_women_conf, results_lung