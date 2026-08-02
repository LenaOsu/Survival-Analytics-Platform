from app.database.repository import get_lung_dataframe
from lifelines import KaplanMeierFitter, WeibullFitter
from lifelines.utils import median_survival_times
from lifelines.statistics import logrank_test
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from lifelines import *



def plot_men_women_survival_prob(kmf, nkmf, wbf, nwbf, sexe, T, E):

    ax1 = plt.subplot(1,1,1)

    kmf.fit(T[sexe], event_observed = E[sexe], label = "Kaplan Meier men")
    kmf.plot_survival_function(ax=ax1, color = "green")

    nkmf.fit(T[~sexe], event_observed = E[~sexe], label = "Kaplan Meier women")
    nkmf.plot_survival_function(ax=ax1, color = "red")

    wbf.fit(T[sexe], event_observed = E[sexe], label = "Weibull men")
    wbf.plot_survival_function(ax=ax1, color = "blue")

    nwbf.fit(T[~sexe], event_observed = E[~sexe], label = "Weibull women")
    nwbf.plot_survival_function(ax=ax1, color = "orange")

    plt.title("Men vs Women status (KM vs Wb)")
    plt.legend()
    plt.savefig("outputs/plots/km_vs_wb.png", dpi=130)
    plt.show()

def hazard_plots(wbf_lung_w, wbf_lung_m):

    t = np.linspace(1, 1000, 200)

    hazard_w = wbf_lung_w.hazard_at_times(t)
    hazard_m = wbf_lung_m.hazard_at_times(t)

    plt.plot(t, hazard_w, label="Women hazard", color = "blue")
    plt.plot(t, hazard_m, label="Men hazard", color = "red")
    plt.title("Weibull hazard function")
    plt.legend()

    plt.savefig("outputs/plots/hazard.png", dpi=130)

    plt.show()