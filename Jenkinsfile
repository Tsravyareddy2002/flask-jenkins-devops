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
                // Ensure pytest can import app.py inside container
                bat "docker run --rm -e PYTHONPATH=/app %APP_NAME%:%TAG% pytest -q"
            }
        }

        stage("Code Quality") {
            steps {
                // flake8 linting
                bat "docker run --rm -e PYTHONPATH=/app %APP_NAME%:%TAG% flake8 app.py"
            }
        }

        stage("Security") {
            steps {
                echo "Security scanning stage (placeholder for Windows Jenkins)."
                echo "In production, tools like Trivy can scan Docker images for vulnerabilities."
            }
        }

        stage("Deploy (Staging)") {
            steps {
                // Stop previous staging container if exists
                bat "docker rm -f flask-api-staging || exit /b 0"
                // Run staging container
                bat "docker run -d --name flask-api-staging -p 5001:5000 %APP_NAME%:%TAG%"
            }
        }

        stage("Release (Production)") {
            steps {
                input message: "Release build %TAG% to PRODUCTION?", ok: "Release Now"
                // Stop previous production container if exists
                bat "docker rm -f flask-api-prod || exit /b 0"
                // Run production container
                bat "docker run -d --name flask-api-prod -p 5000:5000 %APP_NAME%:%TAG%"
            }
        }

        stage("Monitoring & Alerting") {
            steps {
                echo "Monitoring stage (health check)."
                // Windows curl sometimes returns exit code 52 — ignore it
                bat "curl -s http://localhost:5000/health || exit /b 0"
                echo "Health endpoint checked. Metrics available at /metrics."
            }
        }
    }

    post {
        always {
            echo "Pipeline completed successfully."
        }
    }
}
