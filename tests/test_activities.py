def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200

    payload = response.json()
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_adds_new_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}

    activities_response = client.get("/activities")
    assert email in activities_response.json()["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    existing_email = "michael@mergington.edu"

    response = client.post("/activities/Chess%20Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_not_found(client):
    response = client.post("/activities/Nonexistent%20Club/signup", params={"email": "new@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_unregisters_participant(client):
    email = "daniel@mergington.edu"

    response = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}

    activities_response = client.get("/activities")
    assert email not in activities_response.json()["Chess Club"]["participants"]


def test_delete_unknown_activity_returns_not_found(client):
    response = client.delete("/activities/Nonexistent%20Club/participants", params={"email": "x@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_unknown_participant_returns_not_found(client):
    response = client.delete("/activities/Chess%20Club/participants", params={"email": "unknown@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"
