from mongoengine import Document, IntField, StringField, ListField, \
    ReferenceField, DateTimeField, BooleanField, SequenceField, DictField, connect
from config import *
from loguru import logger


# connect to database
connect(DATABASE_NAME,
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        username=DATABASE_LOGIN,
        password=DATABASE_PASSWORD)
logger.info('connect to db')


class ScheduleMain(Document):
    uid = StringField()
    schedule = DictField()


class PostPost(Document):
    post_id = SequenceField()
    text = StringField()
    media = StringField()
    chats = ListField()
    dt_start = DateTimeField()
    dt_last = DateTimeField()
    dt_next = DateTimeField()
    timer = StringField()


class User(Document):
    uid = IntField()
    status = StringField()
    name = StringField()
