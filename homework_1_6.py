import json
import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=60), unique=True, nullable=False)


class Book(Base):
    __tablename__ = "book"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=60), unique=True, nullable=False)
    id_publisher = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="Book")


class Shop(Base):
    __tablename__ = "shop"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=60), unique=True, nullable=False)


class Stock(Base):
    __tablename__ = "stock"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_book = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("book.id"), nullable=False)
    id_shop = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("shop.id"), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    book = relationship(Book, backref="Stock")
    shop = relationship(Shop, backref="Stock")


class Sale(Base):
    __tablename__ = "sale"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=60), unique=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric, nullable=False)
    date_sale = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stock.id"), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    stock = relationship(Stock, backref="Sale")


db_login = 'db_login'
db_password = 'db_password'
db_name = 'db_name'
DSN = 'postgresql://%s:%s@localhost:5432/%s' % (db_login, db_password, db_name)
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()


def create_tables(engine):
    Base.metadata.create_all(engine)


create_tables(engine)


def import_models():
    with open('fixtures/tests_data.json', 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]
        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()


def publisher_search_name():
    search_query = session.query(Publisher).filter(Publisher.name == input("Введите название издателя "))
    for query in search_query.all():
        print(query.id, query.name)


def publisher_search_id():
    search_query = session.query(Publisher).filter(Publisher.id == input("Введите идентификатор (id) издателя "))
    for query in search_query.all():
        print(query.id, query.name)


import_models()
publisher_search_name()
publisher_search_id()
