from email import header
from fastapi.testclient import TestClient

from app import app
import time

client = TestClient(app)

def test_user_login():
    response = client.post("/api/v1/login", json= {'username': 'devismael03', 'password' : 'asd123'})
    assert response.status_code == 200

def test_view_user_detail():
    response = client.post("/api/v1/login", json= {'username': 'devismael03', 'password' : 'asd123'})
    access_token = response.json()["access_token"]

    response2 = client.get("/api/v1/user",headers={"Authorization" : f"Bearer {access_token}"})
    assert response2.status_code == 200
    assert response2.json() == {"username" : "devismael03"}


def test_insert_ip_task():
    login_response = client.post("/api/v1/login", json= {'username': 'devismael03', 'password' : 'asd123'})
    access_token = login_response.json()["access_token"]

    response = client.post("/api/v1/task?ip_address=8.8.8.8", headers={"Authorization" : f"Bearer {access_token}"})
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    time.sleep(2)
    response2 = client.get(f"/api/v1/status?id={task_id}", headers={"Authorization" : f"Bearer {access_token}"})
    assert response2.json()["country"] == "United States"