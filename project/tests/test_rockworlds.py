# project/tests/test_users.py
"""Test all user routes
"""
import json

from project.api.models.rockworld import RockWorld
from project.tests.utils import add_rockworld


def test_add_rockworld_201(test_app, test_database):
    # fmt: off
    world = [
        ". .       ",
        ". . ::::::",
        " :T.::::::",
        ". . ::::::",
        "   .::::::"]
    processedWorld = [
        "  : ::::::",
        "  T ::::::",
        ".   ::::::",
        "::.:::::::"]
    # fmt: on
    client = test_app.test_client()
    resp = client.post(
        "/rockworlds", data=json.dumps(world), content_type="application/json"
    )

    assert resp.status_code == 201
    data = json.loads(resp.data.decode())
    assert data["data"][0]["initialState"] == world
    assert data["data"][0]["finalState"] == processedWorld
    assert "success" in data["status"]


def test_add_random_rockworld_201(test_app, test_database):
    client = test_app.test_client()
    # TODO mock random work generator
    resp = client.post("/rockworlds?random=true&columns=10&rows=10")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "success" in data["status"]


def test_add_rockworld_400_wrong_payload_1(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/rockworlds", data="xyz")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]


def test_add_rockworld_400_wrong_payload_2_list(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/rockworlds", data=json.dumps("asdfsf"), content_type="application/json"
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
    world1 = ["  : ", "  T ", ".   ", "::.:"]
    world = add_rockworld(world=",".join(world1))
    client = test_app.test_client()
    resp = client.get(f"/rockworlds/{world.id}")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert data["data"][0]["initialState"] == world1
    assert "success" in data["status"]


def test_get_rockworlds(test_app, test_database):
    test_database.session.query(RockWorld).delete()
    world1 = ["  : ", "  T ", ".   ", "::.:"]
    world2 = ["  : ", "  T ", ".   ", "::.:"]
    add_rockworld(world=",".join(world1))
    add_rockworld(world=",".join(world2))
    client = test_app.test_client()
    resp = client.get(f"/rockworlds")
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert len(data["data"]) == 2
    assert data["data"][0]["initialState"] == world1
    assert "success" in data["status"]


def test_update_rockworld_incorrect_id(test_app, test_database):
    test_database.session.query(RockWorld).delete()
    client = test_app.test_client()
    resp = client.put("/rockworlds/999", content_type="application/json")
    data = json.loads(resp.data.decode())
    print(data)
    assert resp.status_code == 404
    assert "rockworld 999 does not exist" in data["message"]
    assert "fail" in data["status"]


def test_update_rockworld_invalid_payload_1(test_app, test_database):
    test_database.session.query(RockWorld).delete()
    world1 = ["  : ", "  T ", ".   ", "::.:"]
    world = add_rockworld(world=",".join(world1))
    client = test_app.test_client()
    resp = client.put(
        f"/rockworlds/{world.id}",
        data=json.dumps([".:..", ".TT ", ".bla"]),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Error ValueError: only ' .:T' allowed" in data["message"]
    assert "fail" in data["status"]


def test_update_rockworld_update_success(test_app, test_database):
    test_database.session.query(RockWorld).delete()
    # fmt: off
    initialState = [
        "  : ::::::",
        "  T ::::::",
        ".   ::::::",
        "::.:::::::"
    ]
    newRows = [
        ":  :.     ",
        "    T     "
    ]
    finalState = [
        "    .     ",
        "    T     ",
        "  : ::::::",
        ". T ::::::",
        ":  :::::::",
        "::.:::::::",
    ]
    # fmt: on
    world = add_rockworld(world=",".join(initialState))
    client = test_app.test_client()
    resp = client.put(
        f"/rockworlds/{world.id}",
        data=json.dumps(newRows),
        content_type="application/json",
    )
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert f"rockworld {world.id} updated" in data["message"]
    assert "success" in data["status"]
    assert data["data"][0]["initialState"] == newRows + initialState
    assert data["data"][0]["finalState"] == finalState
