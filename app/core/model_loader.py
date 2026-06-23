from app.models.KaplanMeier import KM_lung
from app.models.Weibull import Wb_lung


def load_models(kmf_lung_m, kmf_lung_w, wbf_lung_m, wbf_lung_w):

    return {
        "male": {
            "km": kmf_lung_m,
            "weibull": wbf_lung_m
        },
        "female": {
            "km": kmf_lung_w,
            "weibull": wbf_lung_w
        }
    }
