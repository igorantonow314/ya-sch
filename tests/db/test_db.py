import datetime
import os

import pytest
import sqlalchemy

from db.db import DB

TEST_DB_NAME = "test-db.db"


def test_db_init():
    db = DB()
    assert db is not None
    del db
    db = DB()
    assert db is not None
    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)
    db = DB(TEST_DB_NAME)
    assert db is not None
    assert os.path.exists(TEST_DB_NAME)
    del db
    assert os.path.exists(TEST_DB_NAME)
    db = DB(TEST_DB_NAME)
    assert db is not None
    assert os.path.exists(TEST_DB_NAME)
    os.remove(TEST_DB_NAME)


@pytest.fixture
def db():
    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)
    return DB(TEST_DB_NAME)


SHOP_UNIT_EXAMPLES = [
    {
        "type": "CATEGORY",
        "name": "Телевизоры",
        "id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "price": 50999,
        "date": datetime.datetime.fromisoformat("2022-02-03T15:00:00.000"),
    },
    {
        "type": "OFFER",
        "name": 'Samson 70" LED UHD Smart',
        "id": "98883e8f-0507-482f-bce2-2fb306cf6483",
        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
        "price": 32999,
        "date": datetime.datetime.fromisoformat("2022-02-03T12:00:00.000"),
    },
]


@pytest.mark.parametrize("shop_unit", SHOP_UNIT_EXAMPLES)
def test_db_insert(db, shop_unit):
    db.insert(**shop_unit)
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db.insert(**shop_unit)


def test_db_insert_all(db):
    for shop_unit in SHOP_UNIT_EXAMPLES:
        db.insert(**shop_unit)
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            db.insert(**shop_unit)


@pytest.mark.parametrize("shop_unit", SHOP_UNIT_EXAMPLES)
def test_db_insert_or_update(db, shop_unit):
    db.insert_or_update(**shop_unit)
    db.insert_or_update(**shop_unit)
    db.insert_or_update(**shop_unit)
