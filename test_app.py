from app import app, calculate_total, calculate_average


def test_total():
    assert calculate_total([80, 90, 70]) == 240


def test_average():
    assert calculate_average([80, 90, 70]) == 80


def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Grade Calculator" in response.data


def test_calculate_post():
    client = app.test_client()
    response = client.post("/", data={"marks": "80 90 70"})
    assert response.status_code == 200
    assert b"Total: 240.0" in response.data
    assert b"Average: 80.0" in response.data


def test_invalid_marks():
    client = app.test_client()
    response = client.post("/", data={"marks": "abc"})
    assert b"Enter valid marks" in response.data


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"
