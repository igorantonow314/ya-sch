import datetime
import os

import pytest
import sqlalchemy

from db.db import DB

TEST_DB_NAME = 'test-db.db'


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
    print('creating new db...')
    if os.path.exists(TEST_DB_NAME):
        os.remove(TEST_DB_NAME)
    return DB(TEST_DB_NAME)


def test_db_insert(db):
    db.insert(
        id="dldl",
        name="test",
        date=datetime.datetime.fromisoformat("2022-06-25T17:53:40"),
        type="CATEGORY",
    )
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        db.insert(
            id="dldl",
            name="test",
            date=datetime.datetime.fromisoformat("2022-06-25T17:53:40"),
            type="CATEGORY",
        )
