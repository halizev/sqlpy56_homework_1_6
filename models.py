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
    publisher = relationship(Publisher, backref="books")


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
    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")


class Sale(Base):
    __tablename__ = "sale"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=60), unique=True)
    price = sqlalchemy.Column(sqlalchemy.Numeric, nullable=False)
    date_sale = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    id_stock = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("stock.id"), nullable=False)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    stock = relationship(Stock, backref="sales")


def create_tables(engine):
    Base.metadata.create_all(engine)