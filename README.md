# Survival Analysis API — Production ML System

Production-ready Machine Learning API for survival analysis using Kaplan-Meier and Weibull models.

The system is deployed in production and exposes a fully documented REST API.

---

## Live System

- 🔗 API: https://survival-analytics-platform.onrender.com  
- 📘 Swagger UI: https://survival-analytics-platform.onrender.com/docs  

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

## Example Request

### Python (recommended)

```python id="r2"
import requests

url = "https://survival-analytics-platform.onrender.com/survival_KM"

payload = {
    "sex": "female",
    "time": 300
}

response = requests.post(url, json=payload)

print(response.json())

## Author:

Léna Osu
Physics PhD | Machine Learning & Statistical Modeling
GitHub: https://github.com/lenaosu
LinkedIn: https://linkedin.com/in/lena-osu-b532073a0