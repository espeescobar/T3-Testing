import hashlib
import pytest
from sqlalchemy import delete

import src.app as app_module
from src.models.models import Quote
from src.scripts.quotes import (
    quote_daily, quotes_get_all, quotes_get, quote_get_by_id, quote_add,
    quote_validate, quote_exists, quote_id_exists, quote_delete,
    quote_tag_exists, quote_tag_add,
)
from src.scripts.tags import (
    tag_add, tag_name_exists, tag_id_exists, tag_delete, tags_get,
    tag_id_get_by_name,
)
from src.scripts.characters import (
    characters_get, character_id_exists, character_has_quotes, character_delete,
)

EINSTEIN_QUOTE = "q1f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4"
EINSTEIN_CHAR = "c1e5d9a8b7f6e4c3d2a1b0c9d8e7f6a5"
AANG_CHAR = "c9g3f7b6a5f4e3d2c1b0a9f8e7d6c5b4"
SCIENCE_TAG = "t1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6"


@pytest.fixture
def db():
    with app_module.app.app_context():
        yield app_module.db


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


# ------------------------------ quotes.py ------------------------------

def test_quote_daily_returns_first_quote_by_id(db):
    q = quote_daily(db)
    assert q["id"] == "q0c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3"
    assert q["character"]["name"] == "Uncle Iroh"
    assert {t["name"] for t in q["tags"]} == {"inspiration", "life", "fantasy", "wisdom"}


def test_quote_daily_without_quotes_returns_empty_dict(db):
    db.session.execute(delete(Quote))
    db.session.commit()
    assert quote_daily(db) == {}


def test_quotes_get_all(db):
    assert len(quotes_get_all(db)) == 9


def test_quotes_get_filters(db):
    assert len(quotes_get(db)) == 9
    assert len(quotes_get(db, character_filter="Einstein")) == 1
    assert len(quotes_get(db, tags_filter=["wisdom"])) == 3
    assert len(quotes_get(db, "Uncle Iroh", ["fantasy", "wisdom"])) == 2
    assert quotes_get(db, tags_filter=["science", "fantasy"]) == []


def test_quote_get_by_id(db):
    q = quote_get_by_id(db, EINSTEIN_QUOTE)
    assert q["character"]["id"] == EINSTEIN_CHAR
    assert len(q["tags"]) == 4
    assert quote_get_by_id(db, "no-existe") is None


def test_quote_add_new_character_and_tags(db):
    res = quote_add(db, {"quote": "Hola", "character": "Nuevo", "source": "S",
                         "tags": ["science", "otra"]})
    assert res["id"] == sha("Hola")
    assert res["character"] == {"id": sha("Nuevo"), "name": "Nuevo"}
    assert {t["name"] for t in res["tags"]} == {"science", "otra"}
    assert quote_id_exists(db, res["id"])
    assert character_id_exists(db, sha("Nuevo"))


def test_quote_add_existing_character_without_tags(db):
    res = quote_add(db, {"quote": "Hola", "character": "Marie Curie", "source": "S"})
    assert res["character"]["id"] == "c3a7f1c0d9b8e6f5a4c3b2a1d0e9f8c7"
    assert res["tags"] == []


def test_quote_add_repeated_tag_is_stored_once(db):
    res = quote_add(db, {"quote": "Hola", "character": "Marie Curie", "source": "S",
                         "tags": ["rep", "rep"]})
    assert len(quote_get_by_id(db, res["id"])["tags"]) == 1


VALID = {"quote": "q", "character": "c", "source": "s"}


def test_quote_validate_ok():
    assert quote_validate(VALID) == {"is_valid": True}
    assert quote_validate({**VALID, "tags": ["a"]}) == {"is_valid": True}


@pytest.mark.parametrize("body", [
    {"quote": "q", "character": "c"},
    {**VALID, "quote": ""}, {**VALID, "quote": 1},
    {**VALID, "character": " "}, {**VALID, "character": None},
    {**VALID, "source": ""}, {**VALID, "source": 2},
    {**VALID, "tags": "a"}, {**VALID, "tags": [""]}, {**VALID, "tags": [3]},
])
def test_quote_validate_invalid(body):
    res = quote_validate(body)
    assert res["is_valid"] is False
    assert res["error"]


def test_quote_exists_and_id_exists(db):
    assert quote_exists(db, "Do what you can, with what you have, where you are.")
    assert not quote_exists(db, "inexistente")
    assert quote_id_exists(db, EINSTEIN_QUOTE)
    assert not quote_id_exists(db, "x")


def test_quote_delete(db):
    quote_delete(db, EINSTEIN_QUOTE)
    assert not quote_id_exists(db, EINSTEIN_QUOTE)
    quote_delete(db, "no-existe")  # no falla
    assert len(quotes_get_all(db)) == 8


def test_quote_tag_exists_and_add(db):
    assert quote_tag_exists(db, EINSTEIN_QUOTE, SCIENCE_TAG)
    new_tag = tag_add(db, "nueva")
    assert not quote_tag_exists(db, EINSTEIN_QUOTE, new_tag)
    quote_tag_add(db, EINSTEIN_QUOTE, new_tag)
    quote_tag_add(db, EINSTEIN_QUOTE, new_tag)  # idempotente
    assert len(quote_get_by_id(db, EINSTEIN_QUOTE)["tags"]) == 5


# ------------------------------ tags.py ------------------------------

def test_tag_add_and_lookups(db):
    assert tag_add(db, "nueva") == sha("nueva")
    assert tag_name_exists(db, "nueva")
    assert tag_id_exists(db, sha("nueva"))
    assert tag_id_get_by_name(db, "nueva") == sha("nueva")
    assert len(tags_get(db)) == 8


def test_tag_lookups_not_found(db):
    assert not tag_name_exists(db, "nada")
    assert not tag_id_exists(db, "nada")
    assert tag_id_get_by_name(db, "nada") is None


def test_tag_delete_removes_relations(db):
    tag_delete(db, SCIENCE_TAG)
    assert not tag_id_exists(db, SCIENCE_TAG)
    assert "science" not in [t["name"] for t in quote_get_by_id(db, EINSTEIN_QUOTE)["tags"]]


# ------------------------------ characters.py ------------------------------

def test_characters_get(db):
    assert len(characters_get(db)) == 9


def test_character_exists_and_has_quotes(db):
    assert character_id_exists(db, EINSTEIN_CHAR)
    assert not character_id_exists(db, "x")
    assert character_has_quotes(db, EINSTEIN_CHAR)
    assert not character_has_quotes(db, AANG_CHAR)


def test_character_delete(db):
    character_delete(db, AANG_CHAR)
    assert not character_id_exists(db, AANG_CHAR)
    character_delete(db, "no-existe")  # no falla
    assert len(characters_get(db)) == 8