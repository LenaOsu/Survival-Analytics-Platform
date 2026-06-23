#API separation + scalable
def compute_survival_KM(model, sex: str, time: int):
#allows to change the model (KM -> Weibull)

    group = model[sex]

    return float(group["km"].predict(time))
    
def compute_survival_Weibull(model, sex: str, time: int):
#allows to change the model (KM -> Weibull)

    group = model[sex]

    return float(group["weibull"].predict(time))
