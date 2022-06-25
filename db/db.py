from copy import deepcopy

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import update

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class ShopUnit(Base):
    __tablename__ = "shop_units"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    parentId = Column(Integer)
    type = Column(String, nullable=False)
    price = Column(Integer)

    def __repr__(self):
        return f"ShopUnit(id={self.id!r}, name={self.name!r}, date={self.date!r})"

    def __eq__(self, other):
        classes_match = isinstance(other, self.__class__)
        a, b = deepcopy(self.__dict__), deepcopy(other.__dict__)
        #compare based on equality our attributes, ignoring SQLAlchemy internal stuff
        a.pop('_sa_instance_state', None)
        b.pop('_sa_instance_state', None)
        attrs_match = (a == b)
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
