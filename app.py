from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST


app = Flask(__name__)


REQUEST_COUNT = Counter(
    "flask_requests_total",
    "Total HTTP requests",
    ["endpoint"]
)


@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    return jsonify(
        {"message": "Flask API is running successfully!"}
    )


@app.route("/health")
def health():
    REQUEST_COUNT.labels(endpoint="/health").inc()
    return jsonify({"status": "healthy"}), 200


@app.route("/metrics")
def metrics():
    REQUEST_COUNT.labels(endpoint="/metrics").inc()
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



