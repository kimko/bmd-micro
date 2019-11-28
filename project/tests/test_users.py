import json


def test_add_user(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "kim", "email": "kimkopowski@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "kimkopowski@gmail.com was added!" in data["message"]
    assert "success" in data["status"]


def test_list_all_users(test_app):
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data["data"]["users"]) > 1
    assert "success" in data["status"]
