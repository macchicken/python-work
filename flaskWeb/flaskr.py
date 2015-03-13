import sqlite3
from contextlib import closing
from flask import Flask, g


# configuration
DATABASE = 'resources/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = '123'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('resources/db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
	print "before request"
	# g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	print "teardown request"
	db = getattr(g, 'db', None)
	if db is not None: db.close()

