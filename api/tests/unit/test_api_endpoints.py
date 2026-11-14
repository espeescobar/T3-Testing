import pytest

# IDs del seed (api/db/init/02_seed.sql)
EINSTEIN_QUOTE = "q1f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4"
CURIE_QUOTE = "q3b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6"
ROOSEVELT_QUOTE = "q4c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7"
EINSTEIN_CHAR = "c1e5d9a8b7f6e4c3d2a1b0c9d8e7f6a5"
AANG_CHAR = "c9g3f7b6a5f4e3d2c1b0a9f8e7d6c5b4"  # sin frases
SCIENCE_TAG = "t1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6"
WISDOM_TAG = "t7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2"

NEW_QUOTE = {
    "quote": "Una frase nueva de prueba",
    "character": "Marie Curie",
    "source": "Speech",
    "tags": ["science", "etiqueta-nueva"],
}


def tag_names(quote):
    return {t["name"] for t in quote["tags"]}


# ---------------------------- Quotes: lectura ----------------------------

def test_get_all_quotes(client):
    resp = client.get("/quotes")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 9
    for q in data:
        assert set(q.keys()) == {"id", "quote", "character", "source", "tags"}


def test_get_quotes_filter_by_character(client):
    data = client.get("/quotes?character=Marie Curie").get_json()
    assert [q["id"] for q in data] == [CURIE_QUOTE]


def test_get_quotes_filter_by_tag(client):
    data = client.get("/quotes?tag=wisdom").get_json()
    assert len(data) == 3
    assert all("wisdom" in tag_names(q) for q in data)


def test_get_quotes_filter_by_multiple_tags_requires_all(client):
    data = client.get("/quotes?tag=science&tag=moustache").get_json()
    assert [q["id"] for q in data] == [EINSTEIN_QUOTE]


def test_get_quotes_filter_character_and_tag(client):
    data = client.get("/quotes?character=Uncle Iroh&tag=fantasy").get_json()
    assert len(data) == 2
    assert all(q["character"]["name"] == "Uncle Iroh" for q in data)


def test_get_quotes_filter_without_matches(client):
    resp = client.get("/quotes?character=Nadie")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_quote_by_id(client):
    resp = client.get(f"/quotes/{EINSTEIN_QUOTE}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == EINSTEIN_QUOTE
    assert data["character"]["name"] == "Albert Einstein"
    assert tag_names(data) == {"science", "inspiration", "life", "moustache"}


def test_get_quote_by_id_not_found(client):
    resp = client.get("/quotes/no-existe")
    assert resp.status_code == 404
    assert "error" in resp.get_json()


# ---------------------------- Quotes: crear ----------------------------

def test_add_quote_success(client):
    resp = client.post("/quotes/add", json=NEW_QUOTE)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["quote"] == NEW_QUOTE["quote"]
    assert data["character"]["name"] == "Marie Curie"
    assert data["character"]["id"] == "c3a7f1c0d9b8e6f5a4c3b2a1d0e9f8c7"
    assert tag_names(data) == {"science", "etiqueta-nueva"}
    assert all("id" in t for t in data["tags"])

    stored = client.get(f"/quotes/{data['id']}")
    assert stored.status_code == 200
    assert stored.get_json()["source"] == "Speech"
    assert len(client.get("/quotes").get_json()) == 10


def test_add_quote_without_tags(client):
    body = {k: v for k, v in NEW_QUOTE.items() if k != "tags"}
    resp = client.post("/quotes/add", json=body)
    assert resp.status_code == 201
    assert resp.get_json()["tags"] == []


def test_add_quote_creates_new_character(client):
    body = {**NEW_QUOTE, "character": "Personaje Nuevo"}
    assert client.post("/quotes/add", json=body).status_code == 201
    names = [c["name"] for c in client.get("/characters").get_json()]
    assert "Personaje Nuevo" in names
    assert len(names) == 10


def test_add_quote_duplicate_returns_409(client):
    assert client.post("/quotes/add", json=NEW_QUOTE).status_code == 201
    resp = client.post("/quotes/add", json=NEW_QUOTE)
    assert resp.status_code == 409
    assert "error" in resp.get_json()
    assert len(client.get("/quotes").get_json()) == 10


@pytest.mark.parametrize("missing", ["quote", "character", "source"])
def test_add_quote_missing_required_field(client, missing):
    body = {k: v for k, v in NEW_QUOTE.items() if k != missing}
    resp = client.post("/quotes/add", json=body)
    assert resp.status_code == 400
    assert "error" in resp.get_json()


@pytest.mark.parametrize(
    "field,value",
    [
        ("quote", ""),
        ("quote", "   "),
        ("quote", 123),
        ("character", ""),
        ("character", None),
        ("source", "  "),
        ("source", 5),
        ("tags", "science"),
        ("tags", [""]),
        ("tags", [1]),
    ],
)
def test_add_quote_invalid_values(client, field, value):
    resp = client.post("/quotes/add", json={**NEW_QUOTE, field: value})
    assert resp.status_code == 400
    assert len(client.get("/quotes").get_json()) == 9


# ---------------------------- Quotes: eliminar ----------------------------

def test_delete_quote_success(client):
    resp = client.delete(f"/quotes/delete/{EINSTEIN_QUOTE}")
    assert resp.status_code == 200
    assert "message" in resp.get_json()
    assert client.get(f"/quotes/{EINSTEIN_QUOTE}").status_code == 404
    assert len(client.get("/quotes").get_json()) == 8


def test_delete_quote_not_found(client):
    resp = client.delete("/quotes/delete/no-existe")
    assert resp.status_code == 404
    assert "error" in resp.get_json()


def test_delete_quote_keeps_character_and_tags(client):
    client.delete(f"/quotes/delete/{EINSTEIN_QUOTE}")
    assert len(client.get("/characters").get_json()) == 9
    assert len(client.get("/tags").get_json()) == 7


# ---------------------------- Tags ----------------------------

def test_get_tags(client):
    resp = client.get("/tags")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 7
    assert {"science", "wisdom", "fantasy"}.issubset({t["name"] for t in data})


def test_add_new_tag_to_quote(client):
    resp = client.post(f"/quotes/{ROOSEVELT_QUOTE}/tags", json={"tags": ["nueva"]})
    assert resp.status_code == 201
    data = resp.get_json()
    assert [t["name"] for t in data] == ["nueva"]
    assert "nueva" in tag_names(client.get(f"/quotes/{ROOSEVELT_QUOTE}").get_json())
    assert "nueva" in {t["name"] for t in client.get("/tags").get_json()}


def test_add_existing_tag_reuses_id(client):
    resp = client.post(f"/quotes/{EINSTEIN_QUOTE}/tags", json={"tags": ["wisdom"]})
    assert resp.status_code == 201
    assert resp.get_json()[0]["id"] == WISDOM_TAG
    assert len(client.get("/tags").get_json()) == 7


def test_add_tag_already_in_quote_does_not_duplicate(client):
    client.post(f"/quotes/{EINSTEIN_QUOTE}/tags", json={"tags": ["science"]})
    quote = client.get(f"/quotes/{EINSTEIN_QUOTE}").get_json()
    assert len(quote["tags"]) == 4


def test_add_tags_quote_not_found(client):
    resp = client.post("/quotes/no-existe/tags", json={"tags": ["x"]})
    assert resp.status_code == 404


def test_add_tags_empty_list(client):
    resp = client.post(f"/quotes/{EINSTEIN_QUOTE}/tags", json={"tags": []})
    assert resp.status_code == 400


@pytest.mark.parametrize("tags", ["wisdom", [1], [None], {"a": 1}])
def test_add_tags_invalid_format(client, tags):
    resp = client.post(f"/quotes/{EINSTEIN_QUOTE}/tags", json={"tags": tags})
    assert resp.status_code == 400


def test_delete_tag_success(client):
    resp = client.delete(f"/tags/delete/{SCIENCE_TAG}")
    assert resp.status_code == 200
    assert len(client.get("/tags").get_json()) == 6
    assert "science" not in tag_names(client.get(f"/quotes/{EINSTEIN_QUOTE}").get_json())


def test_delete_tag_not_found(client):
    resp = client.delete("/tags/delete/no-existe")
    assert resp.status_code == 404
    assert "error" in resp.get_json()


# ---------------------------- Characters ----------------------------

def test_get_characters(client):
    resp = client.get("/characters")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 9
    assert "Albert Einstein" in {c["name"] for c in data}


def test_delete_character_without_quotes(client):
    resp = client.delete(f"/characters/delete/{AANG_CHAR}")
    assert resp.status_code == 200
    ids = [c["id"] for c in client.get("/characters").get_json()]
    assert AANG_CHAR not in ids
    assert len(ids) == 8


def test_delete_character_with_quotes_is_rejected(client):
    resp = client.delete(f"/characters/delete/{EINSTEIN_CHAR}")
    assert resp.status_code == 400
    assert "error" in resp.get_json()
    assert len(client.get("/characters").get_json()) == 9


def test_delete_character_not_found(client):
    resp = client.delete("/characters/delete/no-existe")
    assert resp.status_code == 404


def test_delete_character_after_deleting_its_quote(client):
    client.delete(f"/quotes/delete/{EINSTEIN_QUOTE}")
    resp = client.delete(f"/characters/delete/{EINSTEIN_CHAR}")
    assert resp.status_code == 200