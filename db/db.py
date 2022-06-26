import datetime
import logging
from copy import deepcopy

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import update, delete, select

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session


log = logging.getLogger(__name__)

Base = declarative_base()


def format_date(n):
    res = (
        datetime.datetime.strftime(n, "%Y-%m-%dT%H:%M:%S")
        + datetime.datetime.strftime(n, ".%f")[:4]
        + (datetime.datetime.strftime(n, "%z") or "Z")
    )
    return res


class ShopUnit(Base):
    __tablename__ = "shop_units"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    parentId = Column(Integer)
    type = Column(String, nullable=False)
    price = Column(Integer)

    def as_dict(self):
        ret = {
            "id": self.id,
            "name": self.name,
            "date": format_date(self.date),
            "parentId": self.parentId,
            "type": self.type,
            "price": self.price,
        }
        return ret

    def __repr__(self):
        return f"ShopUnit(id={self.id!r}, name={self.name!r}, date={self.date!r})"

    def __eq__(self, other):
        classes_match = isinstance(other, self.__class__)
        a, b = deepcopy(self.__dict__), deepcopy(other.__dict__)
        # compare based on equality our attributes, ignoring SQLAlchemy internal stuff
        a.pop("_sa_instance_state", None)
        b.pop("_sa_instance_state", None)
        attrs_match = a == b
        return classes_match and attrs_match

    def __ne__(self, other):
        return not self.__eq__(other)


class DB:
    def __init__(self, file="shop.db"):
        self.file = file
        self.engine = create_engine(f"sqlite:///{self.file}")
        Base.metadata.create_all(self.engine)

    def insert(self, **data):
        su = ShopUnit(**data)
        with Session(self.engine) as session:
            session.add(su)
            session.commit()

    def insert_or_update(self, **data):
        su_id = data.pop("id")
        with Session(self.engine) as session:
            if session.get(ShopUnit, su_id):
                session.execute(
                    update(ShopUnit).where(ShopUnit.id == su_id).values(**data)
                )
            else:
                session.add(ShopUnit(id=su_id, **data))
            session.commit()

    def get(self, id):
        with Session(self.engine) as session:
            return session.get(ShopUnit, id)

    def delete(self, id):
        with Session(self.engine) as session:
            if not session.get(ShopUnit, id):
                raise ValueError(f"Element with id {id} was not found")
            session.execute(delete(ShopUnit).where(ShopUnit.id == id))
            session.commit()

    def get_children(self, id):
        with Session(self.engine) as session:
            if session.get(ShopUnit, id) is None:
                raise ValueError(f"ShopUnit with id {id} was not found")
            query = select(ShopUnit.id).where(ShopUnit.parentId == id)
            r = list(session.execute(query))
            if len(r) == 0:
                return None
            return [row[0] for row in r]

    def delete_recursive(self, id):
        stack = [id]
        while stack:
            t = stack.pop(0)
            ch = self.get_children(t)
            if ch:
                stack.extend(ch)
            self.delete(t)
        # note: all children's id (the whole stack) can be obtained with
        # a single sql query
        # TODO: implement this

    def update_date(self, id, datetime):
        with Session(self.engine) as session:
            while id:
                t = session.get(ShopUnit, id)
                if not t:
                    raise ValueError(f"ShopUnit with id {id} was not found")
                session.execute(
                    update(ShopUnit).where(ShopUnit.id == id).values(date=datetime)
                )
                id = t.parentId
            session.commit()
