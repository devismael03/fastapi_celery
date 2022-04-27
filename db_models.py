from peewee import *

mysql_db = MySQLDatabase('whelp', user='root', password='',host='localhost')


class BaseModel(Model):
    class Meta:
        database = mysql_db


class User(BaseModel):
    username = CharField()
    password = CharField()
    class Meta:
        table_name = 'users'

class Task(BaseModel):
    ip = CharField()
    city = CharField()
    country = CharField()
    class Meta:
        table_name = 'tasks'

mysql_db.connect()

mysql_db.create_tables([User,Task])