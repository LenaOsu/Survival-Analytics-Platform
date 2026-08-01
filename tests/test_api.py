
import matplotlib
matplotlib.use("Agg")  # backend non-interactif, ne tente jamais d'ouvrir de fenetre

from fastapi.testclient import TestClient
from app.main import app
from app.api import routes
from app.services.survival import compute_survival_KM, compute_survival_Weibull
from app.main import load_models
from app.models.KaplanMeier import (KM_lung)
from app.models.Weibull import (Wb_lung)

kmf_lung_m, kmf_lung_w, df_lung, T, E, sexe, med_men, med_men_conf, med_women, med_women_conf, results_lung = KM_lung()
wbf_lung_m, wbf_lung_w, df_lung, T, E, sexe, med_men_wb, med_men_conf_wb, med_women_wb, med_women_conf_wb, results_lung_wb = Wb_lung()
model = load_models(kmf_lung_m, kmf_lung_w, wbf_lung_m, wbf_lung_w)

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
