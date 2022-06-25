from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime


class DB:
    def __init__(self, file="shop.db"):
        self.file = file
        self.engine = create_engine(f"sqlite:///{self.file}")
        self.create_db()

    def create_db(self):
        meta = MetaData()

        self.shop_units = Table(
            "shop_units",
            meta,
            Column("id", String, primary_key=True, nullable=False),
            Column("name", String, nullable=False),
            Column("date", DateTime, nullable=False),
            Column("parentId", Integer),
            Column("type", String, nullable=False),
            Column("price", Integer),
        )

        meta.create_all(self.engine)

    def insert(self, **data):
        ins = self.shop_units.insert().values(**data)
        conn = self.engine.connect()
        result = conn.execute(ins)
        return result
