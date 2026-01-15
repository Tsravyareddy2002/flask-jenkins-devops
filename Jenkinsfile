pipeline {
    agent any

    environment {
        APP_NAME = "flask-api"
        TAG = "${env.BUILD_NUMBER}"
        STAGING_URL = "http://localhost:5001/health"
        PROD_URL = "http://localhost:5000/health"
    }

    stages {

        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        stage("Build") {
            steps {
                sh """
                  docker build -t ${APP_NAME}:${TAG} .
                """
            }
        }

        stage("Test") {
            steps {
                sh """
                  docker run --rm ${APP_NAME}:${TAG} pytest -q
                """
            }
        }

        stage("Code Quality") {
            steps {
                sh """
                  docker run --rm ${APP_NAME}:${TAG} flake8 app.py
                """
            }
        }

        stage("Security") {
            steps {
                sh """
                  mkdir -p reports
                  docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ${PWD}:/work aquasec/trivy:latest \
                    image --severity HIGH,CRITICAL --format table --output /work/reports/trivy-report.txt ${APP_NAME}:${TAG} || true

                  echo "---- Trivy Report (HIGH/CRITICAL) ----"
                  cat reports/trivy-report.txt || true
                """
            }
        }

        stage("Deploy (Staging)") {
            steps {
                sh """
                  docker compose -f deploy/docker-compose.staging.yml down || true
                  docker compose -f deploy/docker-compose.staging.yml up -d --build
                  echo "Checking staging health..."
                  for i in 1 2 3 4 5; do
                    curl -sSf ${STAGING_URL} && break || sleep 2
                  done
                """
            }
        }

        stage("Release (Production)") {
            steps {
                input message: "Release build ${TAG} to PRODUCTION?", ok: "Release Now"
                sh """
                  docker tag ${APP_NAME}:${TAG} ${APP_NAME}:${TAG}
                  TAG=${TAG} docker compose -f deploy/docker-compose.prod.yml down || true
                  TAG=${TAG} docker compose -f deploy/docker-compose.prod.yml up -d
                  echo "Checking production health..."
                  for i in 1 2 3 4 5; do
                    curl -sSf ${PROD_URL} && break || sleep 2
                  done
                """
            }
        }

        stage("Monitoring & Alerting") {
            steps {
                sh """
                  echo "Verifying /metrics endpoint..."
                  curl -sSf http://localhost:5000/metrics | head -n 5

                  echo "Starting Prometheus..."
                  docker rm -f prometheus || true
                  docker run -d --name prometheus -p 9090:9090 \
                    -v ${PWD}/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
                    -v ${PWD}/monitoring/alert.rules.yml:/etc/prometheus/alert.rules.yml \
                    prom/prometheus:latest \
                    --config.file=/etc/prometheus/prometheus.yml
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.txt', fingerprint: true
            sh "docker image prune -f || true"
        }
    }
}
