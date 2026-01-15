from app import app

def test_home_endpoint():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert "message" in res.get_json()

def test_health_endpoint():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "healthy"

def test_metrics_endpoint():
    client = app.test_client()
    res = client.get("/metrics")
    assert res.status_code == 200
    assert b"flask_requests_total" in res.data
