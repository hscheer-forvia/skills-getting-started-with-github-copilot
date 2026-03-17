from src.app import activities


def test_signup_success_adds_participant(client):
    email = "new-student@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown%20Club/signup?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_student_returns_400(client):
    existing_email = activities["Chess Club"]["participants"][0]

    response = client.post(f"/activities/Chess%20Club/signup?email={existing_email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_full_activity_returns_400(client):
    activity_name = "Chess Club"
    activities[activity_name]["max_participants"] = len(activities[activity_name]["participants"])

    response = client.post(f"/activities/Chess%20Club/signup?email=another@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
