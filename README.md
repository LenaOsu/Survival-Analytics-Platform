# Survival Analysis API — Production ML System

Production-ready Machine Learning API for survival analysis using Kaplan-Meier and Weibull models.

The system is deployed in production and exposes a fully documented REST API.

---

## Live System

The API is deployed and fully accessible in production.

- API: https://survival-analytics-platform.onrender.com  
- Interactive Swagger Documentation: https://survival-analytics-platform.onrender.com/docs  

The `/docs` endpoint provides full interactive testing of all available routes. 

---

## Overview

This project implements a full machine learning pipeline for survival analysis and exposes it as a production-ready REST API.

It combines statistical modeling, backend engineering, and cloud deployment.

---

## Key Features

- Survival analysis models:
  - Kaplan-Meier estimator (non-parametric)
  - Weibull survival model (parametric)
- REST API built with FastAPI
- Input validation using Pydantic
- Automated testing with pytest
- CI/CD pipeline using GitHub Actions
- Dockerized deployment
- Cloud deployment (Render)

---

## Skills Demonstrated

- Machine Learning: survival analysis, probabilistic modeling
- Backend Engineering: FastAPI REST API design
- MLOps: Docker, CI/CD, cloud deployment
- Software Engineering: modular architecture, testing, API design

---

## API Endpoints

- GET `/health`
- GET `/docs`
- POST `/survival_KM`
- POST `/survival_Weibull`

---

## Design Decisions

**Why FastAPI**
FastAPI was chosen for its high performance, native support for asynchronous operations, and automatic generation of OpenAPI/Swagger documentation, which simplifies API testing and integration.

**Why Kaplan-Meier**
The Kaplan-Meier estimator is a non-parametric method that provides a robust baseline for survival probability estimation without assuming any specific distribution.

**Why Weibull Model**
The Weibull model introduces a parametric approach capable of capturing varying hazard rates over time, making it suitable for modeling more structured time-to-event behaviors.

![Kaplan-Meier vs Weibull Women/Men comparison](./outputs/plots/km_vs_wb.png)

![Weibull Hazard Women/Men comparison plot](./outputs/plots/hazard.png)

**Notable technique points**

- Under/overfitting diagnostics via train/test C-index
- SQL queries using CASE WHEN, aggregate functions, HAVING, and window functions (RANK() OVER (PARTITION BY ...), NTILE()) for cohort segmentation and risk ranking (see app/database/queries/)
- Interactive Power BI dashboard with cross-filtering and conditional formatting (see ./Power Bi Board/PowerBi_survival_analysis.gif)
- Model comparison: Kaplan-Meier (non-parametric baseline) vs Weibull (parametric) vs Cox PH (covariate-based), with visual validation of each model's fit against empirical survival curves on both train and test splits

![Cox vs Kaplan-Meier models](./outputs/plots/cox_vs_km.png)

![Cox vs Weibull models](./outputs/plots/cox_vs_wb.png)

**Why a separation between services / models / API layers**
The architecture follows a modular design to improve maintainability, scalability, and testability:
- `models/` handles statistical and ML logic
- `services/` encapsulates business logic and computations
- `api/` exposes clean REST endpoints via FastAPI

This separation ensures clear responsibilities and simplifies future extensions or model replacement.

---
Running tests:

pytest -v

---
Exporting SQL queries for Power BI:

python -m app.database.run_query

CSV files are written to app/database/outputs/, ready to import into Power BI.

---

## Example Request

### Python 
```python id="r2"
import requests

url = "https://survival-analytics-platform.onrender.com/survival_KM"

payload = {
    "sex": "female",
    "time": 300
}

response = requests.post(url, json=payload)

print(response.json())

***Data source***

lifelines.datasets.load_lung — a public, anonymized lung cancer clinical dataset (North Central Cancer Treatment Group), distributed with the lifelines Python package.

## Author:

Léna Osu
Physics PhD → Statistical Modeling & Inference | Data Science | Self-Taught ML Engineer
GitHub: https://github.com/lenaosu
LinkedIn: https://linkedin.com/in/lena-osu-b532073a0