# configuration
class Config(object):
	DEBUG = False
	SECRET_KEY = 'development key'

class DevelopmentConfig(Config):
	DEBUG = True
	DBSCHEMA = 'resources/db/schema.sql'
	DATABASE = 'resources/tmp/flaskr.db'
	USERNAME = 'admin'
	PASSWORD = '123'