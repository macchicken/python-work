import sqlite3
from contextlib import closing
from flask import Flask, g
from Config import DevelopmentConfig



# create our little application :)
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.logger.addHandler(app.config['LOGHANDLER'])

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(app.config['DBSCHEMA'], mode='r') as f:
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

