from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager, Server
import subprocess, os



SQLALCHEMY_DATABASE_URI = \
    '{engine}://{username}:{password}@{hostname}/{database}'.format(
        engine='mysql+pymysql',
        username=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        hostname=os.getenv('MYSQL_HOST'),
        database=os.getenv('MYSQL_DATABASE'))

app = Flask(__name__, static_url_path='')
if SQLALCHEMY_DATABASE_URI == "mysql+pymysql://None:None@None/None":
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True))
db = SQLAlchemy(app)