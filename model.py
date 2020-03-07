import os
from mongoengine import connect, Document, LongField, IntField, DateTimeField
from dotenv import load_dotenv
load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

connect(DATABASE_NAME, port = int(DATABASE_PORT), host = DATABASE_HOST)

class Statistics(Document):
    player = LongField(primary_key = True, required = True)
    totals = IntField(default = 0, required = False)
    wins = IntField(default = 0, required = False)
    losts = IntField(default = 0, required = False)
    timestamp = DateTimeField(required = False)