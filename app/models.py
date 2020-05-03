from app import app,db,login,bcrypt
from datetime import datetime
import base64
from sqlalchemy import text
from sqlalchemy.dialects.mysql import LONGTEXT
from flask_login import UserMixin


class User(UserMixin, db.Model):

	id = db.Column( db.Integer, primary_key=True )
	username = db.Column( db.String(20), unique=True, index=True )
	password_hash = db.Column( db.String(128) )
	role = db.relationship( "RoleManager", backref="user_obj", lazy="dynamic" )
	report = db.relationship( "Report", backref="user_obj", lazy="dynamic" )
	created_on = db.Column( db.DateTime, default=datetime.now() )
	updated_on = db.Column( db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )

	def set_password(self,password):
		self.password_hash = bcrypt.generate_password_hash( password ).decode("UTF-8")

	def check_password(self,password):
		return bcrypt.check_password_hash( self.password_hash, password )


class RoleManager(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	user = db.Column( db.Integer, db.ForeignKey("user.id") )
	role_no = db.Column( db.Integer, default=100 )
	created_on = db.Column( db.DateTime, default=datetime.now() )
	updated_on = db.Column( db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )


class Report(db.Model):

	id = db.Column( db.Integer, primary_key=True )
	user = db.Column( db.Integer, db.ForeignKey("user.id") )
	report = db.Column( db.Text )
	date = db.Column( db.DateTime, index=True )
	created_on = db.Column( db.DateTime, default=datetime.now() )
	updated_on = db.Column( db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP') )


@login.user_loader
def load_user( user_id ):
	return User.query.get( user_id )