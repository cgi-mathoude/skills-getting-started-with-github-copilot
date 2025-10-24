from fastapi.testclient import TestClient
import pytest

def test_get_activities(client: TestClient):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities

def test_signup_for_activity(client: TestClient):
    """Test signing up for an activity"""
    # Test successful signup
    email = "test@mergington.edu"
    activity_name = "Chess Club"
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

    # Test duplicate signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity(client: TestClient):
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unregister_from_activity(client: TestClient):
    """Test unregistering from an activity"""
    # First sign up a participant
    email = "unregister@mergington.edu"
    activity_name = "Chess Club"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Test successful unregistration
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert "Successfully unregistered" in response.json()["message"]

    # Verify participant was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_nonexistent_activity(client: TestClient):
    """Test unregistering from a non-existent activity"""
    response = client.post("/activities/NonexistentClub/unregister?email=test@mergington.edu")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_unregister_not_registered(client: TestClient):
    """Test unregistering when not registered"""
    response = client.post("/activities/Chess Club/unregister?email=notregistered@mergington.edu")
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"].lower()