"""Tests de integración: secuencias de acciones de un usuario (>= 3 endpoints distintos c/u)."""

NEW = {"quote": "Frase de integración", "character": "Personaje Integración",
       "source": "Fuente", "tags": ["integracion"]}
EINSTEIN_QUOTE = "q1f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4"
EINSTEIN_CHAR = "c1e5d9a8b7f6e4c3d2a1b0c9d8e7f6a5"


def names(items):
    return {i["name"] for i in items}


def test_flow_create_tag_filter_and_delete_quote(client):
    # POST /quotes/add -> GET /quotes/<id> -> POST /quotes/<id>/tags -> GET /quotes?tag= -> DELETE
    qid = client.post("/quotes/add", json=NEW).get_json()["id"]
    assert client.get(f"/quotes/{qid}").get_json()["quote"] == NEW["quote"]

    assert client.post(f"/quotes/{qid}/tags", json={"tags": ["extra"]}).status_code == 201
    found = client.get("/quotes?tag=integracion&tag=extra").get_json()
    assert [q["id"] for q in found] == [qid]

    assert client.delete(f"/quotes/delete/{qid}").status_code == 200
    assert client.get("/quotes?tag=extra").get_json() == []
    assert client.get(f"/quotes/{qid}").status_code == 404


def test_flow_new_character_lifecycle(client):
    # POST /quotes/add -> GET /characters -> DELETE character (400) -> DELETE quote -> DELETE character (200)
    created = client.post("/quotes/add", json=NEW).get_json()
    cid, qid = created["character"]["id"], created["id"]
    assert NEW["character"] in names(client.get("/characters").get_json())

    assert client.delete(f"/characters/delete/{cid}").status_code == 400
    assert client.delete(f"/quotes/delete/{qid}").status_code == 200
    assert client.delete(f"/characters/delete/{cid}").status_code == 200
    assert NEW["character"] not in names(client.get("/characters").get_json())


def test_flow_delete_tag_removes_it_from_quotes(client):
    # POST tags -> GET /tags -> DELETE /tags -> GET /quotes/<id> -> GET /tags
    tag = client.post(f"/quotes/{EINSTEIN_QUOTE}/tags", json={"tags": ["efimera"]}).get_json()[0]
    assert "efimera" in names(client.get("/tags").get_json())
    assert "efimera" in names(client.get(f"/quotes/{EINSTEIN_QUOTE}").get_json()["tags"])

    assert client.delete(f"/tags/delete/{tag['id']}").status_code == 200
    assert "efimera" not in names(client.get(f"/quotes/{EINSTEIN_QUOTE}").get_json()["tags"])
    assert "efimera" not in names(client.get("/tags").get_json())


def test_flow_duplicate_quote_then_recreate_after_delete(client):
    # POST add (201) -> POST add (409) -> GET /quotes -> DELETE -> POST add (201)
    qid = client.post("/quotes/add", json=NEW).get_json()["id"]
    assert client.post("/quotes/add", json=NEW).status_code == 409
    assert len(client.get("/quotes").get_json()) == 10

    assert client.delete(f"/quotes/delete/{qid}").status_code == 200
    assert client.post("/quotes/add", json=NEW).status_code == 201


def test_flow_daily_quote_changes_when_deleted(client):
    # GET /quotes/daily -> GET /quotes/<id> -> DELETE -> GET /quotes/daily
    daily = client.get("/quotes/daily").get_json()
    assert client.get(f"/quotes/{daily['id']}").get_json() == daily

    assert client.delete(f"/quotes/delete/{daily['id']}").status_code == 200
    new_daily = client.get("/quotes/daily").get_json()
    assert new_daily["id"] != daily["id"]


def test_flow_filter_by_character_after_adding_quote(client):
    # POST add (personaje existente) -> GET /quotes?character= -> GET /characters -> DELETE character (400)
    body = {**NEW, "character": "Albert Einstein"}
    qid = client.post("/quotes/add", json=body).get_json()["id"]
    found = client.get("/quotes?character=Albert Einstein").get_json()
    assert {q["id"] for q in found} == {qid, EINSTEIN_QUOTE}
    assert len(client.get("/characters").get_json()) == 9  # no duplicó el personaje
    assert client.delete(f"/characters/delete/{EINSTEIN_CHAR}").status_code == 400