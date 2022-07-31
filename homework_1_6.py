import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

db_login = 'postgres'
db_password = ''
db_name = 'netology_homework'
DSN = 'postgresql://%s:%s@localhost:5432/%s' % (db_login, db_password, db_name)
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

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
    q_join = session.query(Shop).join(Stock).join(Book).join(Publisher)
    q_result = q_join.filter(Publisher.name == input("Введите название (name) издателя "))
    for result in q_result.all():
        print(result.id, result.name)


def publisher_search_id():
    q_join = session.query(Shop).join(Stock).join(Book).join(Publisher)
    q_result = q_join.filter(Publisher.id == input("Введите идентификатор (id) издателя "))
    for result in q_result.all():
        print(result.id, result.name)


import_models()
publisher_search_name()
publisher_search_id()
