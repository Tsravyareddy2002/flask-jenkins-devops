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
                bat "docker run --rm %APP_NAME%:%TAG% pytest -q"
            }
        }

        stage("Code Quality") {
            steps {
                bat "docker run --rm %APP_NAME%:%TAG% flake8 app.py"
            }
        }

        stage("Security") {
            steps {
                echo "Security scanning stage (Trivy placeholder for Windows Jenkins)"
            }
        }

        stage("Deploy (Staging)") {
            steps {
                bat "docker run -d -p 5001:5000 %APP_NAME%:%TAG%"
            }
        }

        stage("Release (Production)") {
            steps {
                input message: "Release build %TAG% to PRODUCTION?", ok: "Release Now"
                bat "docker run -d -p 5000:5000 %APP_NAME%:%TAG%"
            }
        }

        stage("Monitoring & Alerting") {
            steps {
                echo "Monitoring stage (Prometheus placeholder for assignment)"
            }
        }
    }

    post {
        always {
            echo "Pipeline completed"
        }
    }
}
