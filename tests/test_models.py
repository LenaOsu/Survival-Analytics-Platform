from fastapi.testclient import TestClient
from app.main import app
from app.api import routes
from app.services.survival import compute_survival_KM, compute_survival_Weibull
from app.main import load_models
from app.models.KaplanMeier import (KM_lung)
from app.models.Weibull import (Wb_lung)


client = TestClient(app)

kmf_lung_m, kmf_lung_w, df_lung, T, E, sexe, med_men, med_men_conf, med_women, med_women_conf, results_lung = KM_lung()
wbf_lung_m, wbf_lung_w, df_lung, T, E, sexe, med_men_wb, med_men_conf_wb, med_women_wb, med_women_conf_wb, results_lung_wb = Wb_lung()
model = load_models(kmf_lung_m, kmf_lung_w, wbf_lung_m, wbf_lung_w)

def test_km_proba_between_0_and_1():

    prob = compute_survival_KM(model = model, sex = "female", time = 300)
    assert 0 <= prob <=1

def test_weibull_proba_between_0_and_1():

    prob = compute_survival_Weibull(model = model, sex = "female", time = 300)
    assert 0 <= prob <=1

def test_survival_at_time_zero():#proba should always be ~1 at t=0

    prob = compute_survival_KM(model = model, sex = "female", time = 0)
    assert prob > 0.95

def test_sex_female_or_male_ok():

    response = client.post("/survival_KM", json={"sex" : "dog", "time": 300})

    assert response.status_code == 200