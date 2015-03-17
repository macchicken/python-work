from logging.handlers import RotatingFileHandler
import logging

# configuration
class Config(object):
	DEBUG = False
	SECRET_KEY = 'development key'

class DevelopmentConfig(Config):
	DEBUG = True
	DBSCHEMA = 'resources/db/schema.sql'
	DATABASE = 'resources/tmp/flaskr.db'
	LOGGER = 'log/appLog.log'
	LOGHANDLER=RotatingFileHandler(LOGGER,mode='w',maxBytes=1024*1024,backupCount=10)
	LOGHANDLER.setLevel(logging.NOTSET)