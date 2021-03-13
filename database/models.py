from .db import db
import datetime
from mongoengine import *

class Restaurants(db.Document):
    city = db.StringField(required=True, unique=True)
    restaurants = db.ListField(db.StringField(), required=True)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)