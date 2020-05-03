import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

	SECRET_KEY = os.environ.get('SECRET_KEY') or "all_functions_overide_code_10"

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, "database.db")

	# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://admin:9466201496aA@@localhost:3306/reporting'

	SQLALCHEMY_TRACK_MODIFICATIONS = False
