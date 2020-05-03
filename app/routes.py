from app import app
from flask import request,jsonify,url_for,render_template
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app.decorator import Admin
from app.models import *

@app.route("/login_page", methods=["GET","POST"])
def login_page():
	if request.method=="POST":
		if current_user.is_authenticated:
			return jsonify({ "returncode":0, "msg":[ "{} Already Logedin".format( current_user.username ) ] })		
		else:
			if ( "username" in request.form ) and ( "password" in request.form ):
				username = request.form['username']
				password = request.form['password']
				user = User.query.filter_by(username=username).first()
				if user and user.check_password( password ):
					login_user( user )
					return jsonify({ "returncode":0, "msg": [ "{} Login Successfully".format( user.username ) ] })

	return jsonify({ "returncode":1, "error":"invalid username or password" })


@app.route("/logout",methods=["GET","POST"], endpoint="logout")
@login_required
def logout():
	logout_user( current_user )


@app.route("/register",methods=["GET","POST"], endpoint="register")
@login_required
@Admin
def register():
	if request.method=="POST":
		if ( "username" in request.form ) and ( "password" in request.form ):
			user = User( username=request.form["username"] )
			user.set_password( request.form['password'] )
			db.session.add(user)
			db.session.commit()
			return jsonify({ "returncode":0, "msg": [ "{} is Successfully added".format(user.username) ] })

	return jsonify({ "returncode":1, "error":"invalid username or password" })


@app.route("/add_role",methods=["GET","POST"], endpoint="add_role")
@login_required
@Admin
def add_role():
	if request.method=="POST":
		if ( "user" in request.form ) and ( ("role_no" in request.form) and request.form['role_no']<=500 and request.form['role_no']>=100 ):
			user = User.query.filter_by(username=request.form['user']).first()
			role = RoleManager( role_no=request.form['role_no'], user=user.id  )
			db.session.add( role )
			db.session.commit()
			return jsonify({ "returncode":0, "msg": [ "role of {} for user {} has been succesfully added".format(role.role_no,user.username) ] })

	return jsonify({ "returncode":1, "error":"invalid Values" })


@app.route("/add_report",methods=["POST","GET"], endpoint="add_report")
@login_required
@Admin
def  add_report():
	if request.method=="POST":
		if ( "report" in request.form ) :
			msg=[]
			for report in request.form['report']:
				if ( "user" in report ) and ( "report" in report ) and ( "date" in report ):
					user = User.query.filter_by(username=report['user']).first()
					report = Report(user=user.id, report=report['report'], date=datetime.strftime( report['date'], "%Y-%m-%d" ).date() )
					db.session.add(report)
					msg.append( "report of {} for date {} is succesfully submited".format(report.user,report.date) )
				else:
					return jsonify({ "returncode" : 1, "error":"invalid value" })

			db.session.commit()
			return jsonify({ "returncode":0, "msg":msg })

	return jsonify({ "returncode" : 1, "error":"invalid value" })
