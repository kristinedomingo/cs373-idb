#!flask/bin/python
from db import db
from models import Artist, Track, Album
import requests
import json

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

db.create_all();