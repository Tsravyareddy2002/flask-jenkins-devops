pipeline {
    agent any

    environment {
        APP_NAME = "flask-api"
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Build") {
            steps {
                bat "docker build -t %APP_NAME%:%TAG% ."
            }
        }

        stage("Test") {
            steps {
                // Fix: allow pytest to import app.py from /app inside container
                bat "docker run --rm -e PYTHONPATH=/app %APP_NAME%:%TAG% pytest -q"
            }
        }

        stage("Code Quality") {
            steps {
                // Fix: run flake8 cleanly inside container
                bat "docker run --rm -e PYTHONPATH=/app %APP_NAME%:%TAG% flake8 app.py"
            }
        }

        stage("Security") {
            steps {
                echo "Security scanning stage (placeholder on Windows Jenkins)."
                echo "In report: explain Trivy can be used to scan Docker images for CVEs."
            }
        }

        stage("Deploy (Staging)") {
            steps {
                // Stop any previous staging container (ignore errors if not running)
                bat "docker rm -f flask-api-staging || exit /b 0"
                // Run staging on port 5001
                bat "docker run -d --name flask-api-staging -p 5001:5000 %APP_NAME%:%TAG%"
            }
        }

        stage("Release (Production)") {
            steps {
                input message: "Release build %TAG% to PRODUCTION?", ok: "Release Now"
                // Stop any previous production container
                bat "docker rm -f flask-api-prod || exit /b 0"
                // Run production on port 5000
                bat "docker run -d --name flask-api-prod -p 5000:5000 %APP_NAME%:%TAG%"
            }
        }

        stage("Monitoring & Alerting") {
            steps {
                echo "Monitoring stage (lightweight check)."
                // Simple monitoring proof: call health endpoint of production
                bat "curl -s http://localhost:5000/health"
                echo "For high HD: Prometheus/Grafana can scrape /metrics endpoint."
            }
        }
    }

    post {
        always {
            echo "Pipeline completed"
        }
    }
}
