from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
SICK = dict(age=52, sex=1, cp=0, trestbps=125, chol=212, fbs=0, restecg=1,
            thalach=168, exang=0, oldpeak=1, slope=2, ca=2, thal=3)


def test_health():
    assert client.get("/api/health").json()["status"] == "ok"


def test_predict():
    r = client.post("/api/predict", json=SICK)
    assert r.status_code == 200
    d = r.json()
    assert 0 <= d["probability"] <= 1 and d["prediction"] in (0, 1)
    assert len(d["top_factors"]) == 5


def test_validation():
    assert client.post("/api/predict", json={**SICK, "age": 500}).status_code == 422


def test_frontend_served():
    assert "Heart Attack" in client.get("/").text
    assert client.get("/static/app.js").status_code == 200
