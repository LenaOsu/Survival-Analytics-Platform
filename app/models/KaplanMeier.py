from app.src.data_loader import load_survival_data
from lifelines import KaplanMeierFitter
from lifelines.utils import median_survival_times
from lifelines.statistics import logrank_test
from lifelines import *



def KM_lung():

    df_lung, T, E, sexe = load_survival_data()
  
    #have a look on df_lung.groupby("status")["time"].mean() and df.groupby("status")["time"]
    #ALWAYS check the documentation to be sure of the object

   
    kmf_lung_m = KaplanMeierFitter()
    kmf_lung_w = KaplanMeierFitter()
    #print("C")

    kmf_lung_m.fit(T[sexe], event_observed = E[sexe], label = "Men lung disease")
    med_men = kmf_lung_m.median_survival_time_
    med_men_conf = median_survival_times(kmf_lung_m.confidence_interval_)

    kmf_lung_w.fit(T[~sexe], event_observed = E[~sexe], label = "Women lung disease")
    med_women = kmf_lung_w.median_survival_time_
    med_women_conf = median_survival_times(kmf_lung_w.confidence_interval_)

    results_lung = logrank_test(T[sexe], T[~sexe], E[sexe], E[~sexe], alpha=.99)

    return kmf_lung_m, kmf_lung_w, df_lung, T, E, sexe, med_men, med_men_conf, med_women, med_women_conf, results_lung