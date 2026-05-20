from urllib.parse import quote


def test_get_activities(client):
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister(client):
    email = "teststudent@mergington.edu"
    activity = "Chess Club"

    # sign up
    r = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # duplicate signup -> 400
    r2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r2.status_code == 400

    # unregister
    r3 = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert r3.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_signup_nonexistent_activity(client):
    r = client.post(f"/activities/{quote('NoSuchActivity')}/signup", params={"email": "x@y.com"})
    assert r.status_code == 404


def test_unregister_not_signed_up(client):
    r = client.delete(f"/activities/{quote('Programming Class')}/participants", params={"email": "not@here.com"})
    assert r.status_code == 404
