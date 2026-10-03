from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["application"] == "TaskFlow API"
    assert data["status"] == "running"


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_get_tasks():
    client = app.test_client()
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
