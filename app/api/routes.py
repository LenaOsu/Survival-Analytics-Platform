from fastapi import APIRouter
from app.schemas.request import SurvivalRequest
from app.services.survival import compute_survival_KM, compute_survival_Weibull
from app.core.model_loader import load_models
from app.models.KaplanMeier import (KM_lung)
from app.models.Weibull import (Wb_lung)
from app.core.config import MODEL_VERSION

kmf_lung_m, kmf_lung_w, df_lung, T, E, sexe, med_men, med_men_conf, med_women, med_women_conf, results_lung = KM_lung()
wbf_lung_m, wbf_lung_w, df_lung, T, E, sexe, med_men_wb, med_men_conf_wb, med_women_wb, med_women_conf_wb, results_lung_wb = Wb_lung()
model = load_models(kmf_lung_m, kmf_lung_w, wbf_lung_m, wbf_lung_w)
router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "model_version": MODEL_VERSION}

@router.post("/survival_KM")
def survival_km(req: SurvivalRequest):
    prob = compute_survival_KM(model, req.sex, req.time)
    return {
        "sex": req.sex,
        "time": req.time,
        "survival_probability": prob
    }
    
@router.post("/survival_Weibull")
def survival_wb(req: SurvivalRequest):
    prob = compute_survival_Weibull(model, req.sex, req.time)
    return {
        "sex": req.sex,
        "time": req.time,
        "survival_probability": prob
    }
