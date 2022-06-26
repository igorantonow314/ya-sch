import datetime
import os

import pytest
import sqlalchemy

from db.db import DB, ShopUnit

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
        "name": "Товары",
        "id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "price": 58599,
        "parentId": None,
        "date": datetime.datetime.fromisoformat("2022-02-03T15:00:00.000"),
    },
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
    {
        "type": "OFFER",
        "name": 'Phyllis 50" LED UHD Smarter',
        "id": "74b81fda-9cdc-4b63-8927-c978afed5cf4",
        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
        "price": 49999,
        "date": datetime.datetime.fromisoformat("2022-02-03T12:00:00.000"),
    },
    {
        "type": "OFFER",
        "name": 'Goldstar 65" LED UHD LOL Very Smart',
        "id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
        "parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
        "price": 69999,
        "date": datetime.datetime.fromisoformat("2022-02-03T15:00:00.000"),
    },
    {
        "type": "CATEGORY",
        "name": "Смартфоны",
        "id": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1",
        "price": 69999,
        "date": datetime.datetime.fromisoformat("2022-02-02T12:00:00.000"),
    },
    {
        "type": "OFFER",
        "name": "jPhone 13",
        "id": "863e1a7a-1304-42ae-943b-179184c077e3",
        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "price": 79999,
        "date": datetime.datetime.fromisoformat("2022-02-02T12:00:00.000"),
    },
    {
        "type": "OFFER",
        "name": "Xomiа Readme 10",
        "id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
        "parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2",
        "price": 59999,
        "date": datetime.datetime.fromisoformat("2022-02-02T12:00:00.000"),
    },
]


@pytest.mark.parametrize("shop_unit", SHOP_UNIT_EXAMPLES)
def test_equals(shop_unit):
    assert ShopUnit(**shop_unit) == ShopUnit(**shop_unit)


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


def test_db_get(db):
    for shop_unit in SHOP_UNIT_EXAMPLES:
        db.insert(**shop_unit)
        s = db.get(id=shop_unit["id"])
        assert s == ShopUnit(**shop_unit)
    for shop_unit in SHOP_UNIT_EXAMPLES:
        s = db.get(id=shop_unit["id"])
        assert s == ShopUnit(**shop_unit)
    for shop_unit in SHOP_UNIT_EXAMPLES:
        db.insert_or_update(**shop_unit)
        s = db.get(id=shop_unit["id"])
        assert s == ShopUnit(**shop_unit)


@pytest.mark.parametrize("shop_unit", SHOP_UNIT_EXAMPLES)
def test_db_delete_one(db, shop_unit):
    db.insert(**shop_unit)
    assert db.get(shop_unit["id"]) == ShopUnit(**shop_unit)
    db.delete(shop_unit["id"])
    assert db.get(shop_unit["id"]) is None
    with pytest.raises(ValueError):
        db.delete(shop_unit["id"])


def test_db_delete(db):
    db.insert(**SHOP_UNIT_EXAMPLES[0])
    db.insert(**SHOP_UNIT_EXAMPLES[1])
    db.delete(SHOP_UNIT_EXAMPLES[0]["id"])
    with pytest.raises(ValueError):
        db.delete(SHOP_UNIT_EXAMPLES[0]["id"])
    db.delete(SHOP_UNIT_EXAMPLES[1]["id"])
    with pytest.raises(ValueError):
        db.delete(SHOP_UNIT_EXAMPLES[1]["id"])


def test_db_delete_2(db):
    db.insert(**SHOP_UNIT_EXAMPLES[1])
    db.insert(**SHOP_UNIT_EXAMPLES[0])
    db.delete(SHOP_UNIT_EXAMPLES[0]["id"])
    with pytest.raises(ValueError):
        db.delete(SHOP_UNIT_EXAMPLES[0]["id"])
    db.delete(SHOP_UNIT_EXAMPLES[1]["id"])
    with pytest.raises(ValueError):
        db.delete(SHOP_UNIT_EXAMPLES[1]["id"])


def test_db_get_children(db):
    for shop_unit in SHOP_UNIT_EXAMPLES:
        db.insert(**shop_unit)
    # Товары: телевизоры, смартфоны
    assert db.get_children("069cb8d7-bbdd-47d3-ad8f-82ef4c269df1") == [
        "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
        "d515e43f-f3f6-4471-bb77-6b455017a2d2",
    ]
    # Смартфоны: jPhone 13, Xomia Readme 10
    assert db.get_children("d515e43f-f3f6-4471-bb77-6b455017a2d2") == [
        "863e1a7a-1304-42ae-943b-179184c077e3",
        "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4",
    ]
    # jPhone 13: это OFFER
    assert db.get_children("b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4") is None
    # Телевизоры: ...
    assert db.get_children("1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2") == [
        "98883e8f-0507-482f-bce2-2fb306cf6483",
        "74b81fda-9cdc-4b63-8927-c978afed5cf4",
        "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
    ]
    db.delete("73bc3b36-02d1-4245-ab35-3106c9ee1c65")
    assert db.get_children("1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2") == [
        "98883e8f-0507-482f-bce2-2fb306cf6483",
        "74b81fda-9cdc-4b63-8927-c978afed5cf4",
    ]
    # Samson 70: это OFFER
    assert db.get_children("98883e8f-0507-482f-bce2-2fb306cf6483") is None
    # Несуществующий товар
    with pytest.raises(ValueError):
        db.get_children("non-valid-id")
    db.delete("1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2")  # телевизоры
    with pytest.raises(ValueError):
        db.get_children("1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2")


def test_delete_recursive(db):
    for shop_unit in SHOP_UNIT_EXAMPLES:
        db.insert(**shop_unit)

    # Удаление смартфонов
    db.delete_recursive("d515e43f-f3f6-4471-bb77-6b455017a2d2")
    assert db.get("d515e43f-f3f6-4471-bb77-6b455017a2d2") is None  # Смартфоны удалены
    assert db.get("863e1a7a-1304-42ae-943b-179184c077e3") is None  # jPhone 13 удалён
    assert db.get("b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4") is None  # Xomia удалён
    # Товары: телевизоры, нет смартфонов
    assert db.get_children("069cb8d7-bbdd-47d3-ad8f-82ef4c269df1") == [
        "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2",
    ]
    # Телевизоры: в сохранности
    assert db.get_children("1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2") == [
        "98883e8f-0507-482f-bce2-2fb306cf6483",
        "74b81fda-9cdc-4b63-8927-c978afed5cf4",
        "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
    ]

    # Удаление OFFER: Samson 70
    db.delete_recursive("98883e8f-0507-482f-bce2-2fb306cf6483")
    assert db.get("98883e8f-0507-482f-bce2-2fb306cf6483") is None  # Samson 70 удалён
    # телевизоры:
    assert db.get_children("1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2") == [
        "74b81fda-9cdc-4b63-8927-c978afed5cf4",
        "73bc3b36-02d1-4245-ab35-3106c9ee1c65",
    ]

    # Удаление оставшихся телевизоров
    db.delete_recursive("1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2")
    assert db.get("1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2") is None  # телевизоры удалены
    assert db.get("74b81fda-9cdc-4b63-8927-c978afed5cf4") is None  # Phyllis удалён
    assert db.get("73bc3b36-02d1-4245-ab35-3106c9ee1c65") is None  # Goldstar 65 удалён
    assert db.get("98883e8f-0507-482f-bce2-2fb306cf6483") is None  # Samson давно удалён
    # Категорий товаров не осталось:
    assert db.get_children("069cb8d7-bbdd-47d3-ad8f-82ef4c269df1") is None

    # Удаление несуществующего элемента
    with pytest.raises(ValueError):
        db.delete_recursive("98883e8f-0507-482f-bce2-2fb306cf6483")  # Samson 70
    with pytest.raises(ValueError):
        db.delete_recursive("non-valid-id")
