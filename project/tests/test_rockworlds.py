# project/tests/test_users.py
"""Test all user routes
"""
import json

from project.api.models.rockworld import RockWorld
from project.tests.utils import add_rockworld


def test_add_rockworld_201(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/rockworlds",
        data=json.dumps(
            [
                ". .       ",
                ". . ::::::",
                " :T.::::::",
                ". . ::::::",
                "   .::::::",
            ]
        ),
        content_type="application/json",
    )
    # This is a lie
    processedWorld = [
        ". .       ",
        ". . ::::::",
        " :T.::::::",
        ". . ::::::",
        "   .::::::",
    ]

    # Actual Test
    # processedWorld = ["  : ::::::", "  T ::::::", ".   ::::::", "::.:::::::"]
    assert resp.status_code == 201
    data = json.loads(resp.data.decode())
    assert data["data"][0]["world"] == processedWorld
    assert "success" in data["status"]


def test_add_rockworld_400_wrong_payload_1(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/rockworlds",
        data='xyz',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_rockworld_400_wrong_payload_2_list(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/rockworlds",
        data=json.dumps("asdfsf"),
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = json.loads(resp.data.decode())
    assert "Invalid payload. ValueError: list expected" in data["message"]
    assert "fail" in data["status"]


def test_add_rockworld_400_wrong_payload_3_list_shape(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/rockworlds",
        data=json.dumps(
            [
                ". .       ",
                ". . :::::::::::::::::::::",
                " :T.::::::",
                ". . ::::::",
                "   .::::::",
            ]
        ),
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = json.loads(resp.data.decode())
    assert "Invalid payload. ValueError: wrong list shape" in data["message"]
    assert "fail" in data["status"]


def test_add_rockworld_400_wrong_payload_4_invalid_content(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/rockworlds",
        data=json.dumps([".:.", "TT ", "bla"]),
        content_type="application/json",
    )
    assert resp.status_code == 400
    data = json.loads(resp.data.decode())
    assert "Invalid payload. ValueError: only ' .:T' allowed" in data["message"]
    assert "fail" in data["status"]


def test_get_rockworld(test_app, test_database):
    finalWorld = ["  : ", "  T ", ".   ", "::.:"]
    world = add_rockworld(world=",".join(finalWorld))
    client = test_app.test_client()
    resp = client.get(f"/rockworlds/{world.id}")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert data["data"][0]["world"] == finalWorld
    assert "success" in data["status"]


def test_get_rockworlds(test_app, test_database):
    test_database.session.query(RockWorld).delete()
    finalWorld = ["  : ", "  T ", ".   ", "::.:"]
    finalWorld2 = ["  : ", "  T ", ".   ", "::.:"]
    add_rockworld(world=",".join(finalWorld))
    add_rockworld(world=",".join(finalWorld2))
    client = test_app.test_client()
    resp = client.get(f"/rockworlds")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert len(data["data"]) == 2
    assert data["data"][0]["world"] == finalWorld
    assert "success" in data["status"]
