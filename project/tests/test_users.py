# project/tests/test_users.py
"""Test all user routes
"""
import json

from project.tests.utils import add_user


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps(
            {
                "lastName": "Kopowski",
                "firstName": "Kim",
                "email": "kimkopowski@gmail.com",
                "zipCode": "97202",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "kimkopowski@gmail.com was added!" in data["message"]
    assert "success" in data["status"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/users", data=json.dumps({}), content_type="application/json")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"notaRealField": "meh"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"firstName": "kim", "email": "kim@blurgh.io"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"firstName": "kim", "email": "kim@blurgh.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "User with email kim@blurgh.io already exists." in data["message"]
    assert "fail" in data["status"]


def test_single_user(test_app, test_database):
    user = add_user(email="single@blurgh.io", firstName="single")
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "single" in data["data"]["firstName"]
    assert "single@blurgh.io" in data["data"]["email"]
    assert "success" in data["status"]


def test_single_user_wrong_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/blah")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User does not exist" in data["message"]
    assert "fail" in data["status"]


def test_list_all_users(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data["data"]["users"]) > 0
    assert "success" in data["status"]


def test_remove_user(test_app, test_database):
    user = add_user(firstName="user-to-be-removed", email="remove-me@meh.io")
    client = test_app.test_client()
    resp_one = client.get(f"/users/{user.id}")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    resp_two = client.delete(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "remove-me@meh.io was removed!" in data["message"]
    assert "success" in data["status"]
    resp_three = client.get(f"/users/{user.id}")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 404


def test_remove_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User does not exist" in data["message"]
    assert "fail" in data["status"]


def test_remove_user_invalid_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/users/x")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_update_user(test_app, test_database):
    user = add_user(firstName="user-to-be-updated", email="update-me@meh.io")
    client = test_app.test_client()
    resp_one = client.put(
        f"/users/{user.id}",
        data=json.dumps({"firstName": "me", "email": "update-me@meh.io"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{user.id} was updated!" in data["message"]
    assert "success" in data["status"]
    resp_two = client.get(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "me" in data["data"]["firstName"]
    assert "update-me@meh.io" in data["data"]["email"]
    assert "success" in data["status"]


def test_update_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/users/999",
        data=json.dumps({"firstName": "me", "email": "update-me@meh.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User does not exist" in data["message"]
    assert "fail" in data["status"]


def test_update_user_invalid_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/users/nein",
        data=json.dumps({"firstName": "me", "email": "update-me@meh.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_update_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.put(
        "/users/999", data=json.dumps({}), content_type="application/json"
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
