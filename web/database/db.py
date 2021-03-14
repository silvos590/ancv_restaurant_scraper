from flask_mongoengine import MongoEngine

db = MongoEngine()

def initialize_db(app):
    db.init_app(app)

# This method i just for development phase
def drop_db(app):
    db.connection.drop_database('my_db')