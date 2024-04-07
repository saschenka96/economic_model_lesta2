import sqlite3
from peewee import *

db = SqliteDatabase('accounts.db')


class Accounts(Model):
    id = PrimaryKeyField(unique=True)
    nickname = CharField()
    credits = FloatField()
    items = CharField()

    class Meta:
        database = db
        db_table = 'Accounts'
        order_by = 'id'
