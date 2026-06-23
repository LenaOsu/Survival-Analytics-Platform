from lifelines.datasets import load_dd, load_waltons, load_lung
from lifelines import KaplanMeierFitter, WeibullFitter
from lifelines.utils import median_survival_times
from lifelines.statistics import logrank_test
from matplotlib import pyplot as plt
import pandas as pd
from lifelines import *
from app.models.KaplanMeier import (democracy_KM, KM_lung)
from app.models.Weibull import (democracy_Wb, Wb_lung)
from app.src.features import (error_model, horizon_probability, death_risk, summary)
from app.src.visualization import (plot_MK_Wb_democracy, plot_men_women_survival_prob, hazard_plots)

from fastapi import FastAPI
from app.api.routes import router
from app.core.model_loader import load_models


def main():

    #apetizer !
    kmf_democracy, kmf_ndemocracy, dem, T, E, med_dem, med_dem_conf, med_ndem, med_ndem_conf, results = democracy_KM()
    wbf_democracy, wbf_ndemocracy, df, _, T, E, med_dem_w, med_dem_conf_w, med_ndem_w, med_ndem_conf_w, results_w = democracy_Wb()
    plot_MK_Wb_democracy(kmf_democracy, kmf_ndemocracy, wbf_democracy, wbf_ndemocracy, dem, T, E)

    #practical case :)
    kmf_lung_m, kmf_lung_w, df_lung, T, E, sexe, med_men, med_men_conf, med_women, med_women_conf, results_lung = KM_lung()
    wbf_lung_m, wbf_lung_w, df_lung, T, E, sexe, med_men_wb, med_men_conf_wb, med_women_wb, med_women_conf_wb, results_lung_wb = Wb_lung()
    plot_men_women_survival_prob(kmf_lung_m, kmf_lung_w, wbf_lung_m, wbf_lung_w, sexe, T, E)

    print("QUESTION : What is the probability that a women or a male patient survive at time=300 days ?")

    answer = kmf_lung_w.survival_function_at_times(300)
    answer_wb = wbf_lung_w.survival_function_at_times(300)

    second_answer = kmf_lung_m.survival_function_at_times(300)
    second_answer_wb = wbf_lung_m.survival_function_at_times(300)

    print("type answer:",type(answer))
    answer_value = answer.iloc[0]
    print("answer value is :", answer_value)

    print(f"Kaplan Meier survival probabilities at t=300 days : {answer*100} for women and {second_answer*100} for male.")
    print(f"Weibull survival probabilities at t=300 days : {answer_wb*100} for women and {second_answer_wb*100} for male.")

    print("-------------- Women Weibull fitter lung data summary:")
    wbf_lung_w.print_summary()

    print("-------------- Men Weibull fitter lung data summary:")
    wbf_lung_m.print_summary()

    print("Weibull Women Results involve that shape parameter (p = 1.57) are significantly different from 1 (p-value <0.005 for rho/lambda for women and z = 3.34)." \
    "This indicates that the hazard function is NOT constant over time. The positive deviation from 1 suggests an increasing failure rate." \
    "This is coherent with a deterioration process. ")

    print("Meanwhile, Weibull men results involve that lambda is statistically significant, indicating a well-defined survival time scale." \
    "Whereas, the shape parameter rho is not significantly different from the reference value, suggesting insufficient proof for an increasing deterioration (p < 0.1)." \
    "This could means that the mortality risk for men is approximately constant over time, or that the dataset lacks power to detect time variation.")

    print("median Kaplan Meier women survival time : ", med_women)
    print("median Weibull women survival time : ", med_women_wb)

    print("median Kaplan Meier men survival time : ", med_men)
    print("median Weibull men survival time : ", med_men_wb)

    print("KM approximates very well Weibull. " \
    "NOTE : A better global survival time for women (~420 > 260).")

    print("Kaplan Meier women confidence interval : ", med_women_conf)
    print("Weibull women confidence interval : ", med_women_conf_wb)
    print("Kaplan Meier men confidence interval : ", med_men_conf)
    print("Weibull men confidence interval : ", med_men_conf_wb)

    print("CONCLUSION : The Weibull confidence intervals for median survival are not bounded, indicating instability in parametric uncertainty estimation, likely due to censoring and limited tail information.")

    km_w, wb_w, km_m, wb_m = error_model(kmf_lung_w, wbf_lung_w, kmf_lung_m, wbf_lung_m)

    print("GOOD agreement between KM and Weibull models. Even better coherence for men.")

    horizon_probability(kmf_lung_w, kmf_lung_m) #use predict instead

    hazard_plots(wbf_lung_w, wbf_lung_m)
    print("Slower deterioration for women. Bigger risk for men, deterioration more aggressive.")

    print("What are the death risks for both men and women before t = 365 days ?")
    death_risk(wbf_lung_w, wbf_lung_m)

    print("---------------------------- TO RECAP ------------------------------")

    summary(med_women, med_women_wb, med_men, med_men_wb, wbf_lung_w, wbf_lung_m, kmf_lung_w, kmf_lung_m)

    print("MODEL STAT DONE.")
    print("Let's build the API.")

app = FastAPI(
    title="Survival Analytics API",
    docs_url="/docs",   # désactiver en prod plus tard
)


app.include_router(router)

#kmf_lung_m, kmf_lung_w, df_lung, T, E, sexe, med_men, med_men_conf, med_women, med_women_conf, results_lung = KM_lung()
#wbf_lung_m, wbf_lung_w, df_lung, T, E, sexe, med_men_wb, med_men_conf_wb, med_women_wb, med_women_conf_wb, results_lung_wb = Wb_lung()



if __name__ == "__main__":
    main()