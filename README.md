# Flask Jenkins DevOps Pipeline Project

## Overview
This project is a simple **Python Flask REST API** developed to demonstrate a complete **CI/CD DevOps pipeline** using **Jenkins, Docker, and GitHub**.

The focus of this project is not application complexity, but the implementation of DevOps practices such as automated build, testing, security scanning, deployment, release management, and monitoring.

This project is created as part of the **SIT223 / SIT753 DevOps assignment**.

---

## Project Architecture

- Source code is managed using **GitHub**
- **Jenkins** automates the CI/CD pipeline
- **Docker** is used to build and deploy the application
- **Prometheus** is used for monitoring and alerting

---

## Application Description
The application is a lightweight **Flask-based REST API** that exposes the following endpoints:

| Endpoint | Description |
|--------|------------|
| `/` | Home endpoint to verify the application is running |
| `/health` | Health check endpoint used for deployment verification |
| `/metrics` | Metrics endpoint used by Prometheus for monitoring |

The application is intentionally kept simple so that the focus remains on DevOps automation rather than business logic.

---

## Folder Structure
flask-jenkins-devops/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── README.md
├── tests/
│ └── test_app.py
├── deploy/
│ ├── docker-compose.staging.yml
│ └── docker-compose.prod.yml
└── monitoring/
├── prometheus.yml
└── alert.rules.yml

---

## Technologies Used
- Python 3.11
- Flask
- Pytest
- Flake8
- Docker
- Docker Compose
- Jenkins
- Trivy
- Prometheus

---

## Jenkins Pipeline Stages
The Jenkins pipeline implements the following stages:

1. **Checkout** – Fetches source code from GitHub  
2. **Build** – Builds a Docker image for the Flask application  
3. **Test** – Runs automated tests using Pytest  
4. **Code Quality** – Performs static code analysis using Flake8  
5. **Security** – Scans the Docker image for vulnerabilities using Trivy  
6. **Deploy (Staging)** – Deploys the application to a staging environment  
7. **Release (Production)** – Promotes the application to production with manual approval  
8. **Monitoring & Alerting** – Monitors the production application using Prometheus  

---

## How to Run the Application Locally

### Install dependencies
```bash
pip install -r requirements.txt
Run the Flask application
python app.py


Open in browser:

http://localhost:5000/

http://localhost:5000/health

http://localhost:5000/metrics

How to Run Using Docker
Build Docker image
docker build -t flask-api .

Run Docker container
docker run -p 5000:5000 flask-api
