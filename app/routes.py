from app import app
from flask import request,jsonify,url_for,render_template
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app.decorator import Admin
from app.models import *
import re

def valid_date(datestring):
	try:
		mat=re.match('(\d{4})[/.-](\d{2})[/.-](\d{2})$', datestring)
		if mat is not None:
				datetime(*(map(int, mat.groups())))
				return True
	except ValueError:
			pass
	return False

@app.route("/check_server", methods=["GET"])
def check_server():
	return jsonify({ "returncode" : 0 })


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


@app.route("/register", methods=["GET","POST"], endpoint="register")
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


@app.route("/add_role", methods=["GET","POST"], endpoint="add_role")
@login_required
@Admin
def add_role():
	if request.method=="POST":
		data = request.get_json()
		if request.is_json and ( "username" in data ) and ("role_no" in data):
			if  data["role_no"].isnumeric() and int(data['role_no'])<=500 and int(data['role_no'])>=100:
				user = User.query.filter_by(username=data['username']).first()
				if user:
					role = RoleManager( role_no=int(data['role_no']), user=user.id  )
					db.session.add( role )
					db.session.commit()
					return jsonify({ "returncode":0, "msg": [ "role of {} for user {} has been succesfully added".format(role.role_no,user.username) ] })

	return jsonify({ "returncode":1, "error":"invalid Values" })


@app.route("/add_report", methods=["POST","GET"], endpoint="add_report")
@login_required
@Admin
def  add_report():
	if request.method=="POST":
		if request.is_json and ( "report" in request.get_json() ) :
			msg=[]
			for report in request.get_json()['report']:
				if ( "username" in report ) and ( "report" in report ) and ( "date" in report ):
					user = User.query.filter_by(username=report['username']).first()
					if user and valid_date( report['date'] ):
						date = datetime.strptime( report['date'], "%Y-%m-%d" ).date()
						print( Report.query.filter_by(user=user.id,date=date).first(), report )
						if not Report.query.filter_by(user=user.id,date=date).first():
							report = Report(user=user.id, report=report['report'], date=date )
							db.session.add(report)
							msg.append( "report of {} for date {} is succesfully submited".format(user.username,report.date) )
						else:
							return jsonify({ "returncode" : 1, "error":"Same date reporting exists for {}".format(user.username) })
					else:
						return jsonify({ "returncode" : 1, "error":"invalid value" })
				else:
					return jsonify({ "returncode" : 1, "error":"invalid value" })

			db.session.commit()
			return jsonify({ "returncode":0, "msg":msg })

	return jsonify({ "returncode" : 1, "error":"invalid value" })

@app.route("/fetch_user", methods=["GET"], endpoint="fetch_user")
@login_required
@Admin
def fetch_user():
	user_list = [ user.username for user in User.query.all() ]
	return jsonify({ "returncode" : 0, "user_list" : user_list, "count" : len(user_list) })


@app.route("/fetch_reporting", methods=["GET","POST"], endpoint="fetch_reporting")
@login_required
@Admin
def fetch_reporting():
	if request.method=="POST" and request.is_json:
		data = request.get_json()
		if ( "user_list" in data ) and ( "filter" in data ):
			user_list = []
			for username in data['user_list']:

				user = User.query.filter_by(username=username).first()
				if user:
					user_list.append( user )
				else:
					return jsonify({ "returncode" : 1, "error" : "invalid user" })


			_filter_ = data['filter']
			reporting_count = 0

			if "date" not in _filter_:
				reporting = {}
				for user in user_list:
					user_report = user.report.order_by( Report.date.desc() ).all()
					report_list = []
					for j in user_report:
						report_list.append( [ j.id, j.report, j.date.strftime("%d %b %Y") ] )
						reporting_count+=1

					reporting[ user.username ]=report_list

				return jsonify({ "returncode" : 0, "reporting" : reporting, "msg" : [ "{} reporting fetched".format(reporting_count) ]  })
			else:
				reporting = {}
				for user in user_list:

					if valid_date( _filter_['date'][0] ):
						start_date = datetime.strptime( _filter_['date'][0], "%Y-%m-%d" ).date()
					elif _filter_['date'][0]=="":
						start_date = None
					else:
						return jsonify({ "returncode" : 1, "error" : "invalid date" })

					if valid_date( _filter_['date'][1] ):
						end_date = datetime.strptime( _filter_['date'][1], "%Y-%m-%d" ).date()
					elif _filter_['date'][1]=="":
						end_date = None
					else:
						return jsonify({ "returncode" : 1, "error" : "invalid date" })


					if start_date:
						if end_date:
							user_report = user.report.filter( Report.date >= start_date, Report.date <= end_date ).order_by( Report.date.desc() ).all()
							report_list = []
							for j in user_report:
								report_list.append( [ j.id, j.report, j.date.strftime("%d %b %Y") ] )
								reporting_count+=1

							reporting[ user.username ]=report_list
						else:
							user_report = user.report.filter( Report.date >= start_date ).order_by( Report.date.desc() ).all()
							report_list = []
							for j in user_report:
								report_list.append( [ j.id, j.report, j.date.strftime("%d %b %Y") ] )
								reporting_count+=1

							reporting[ user.username ]=report_list
					else:
						if end_date:
							user_report = user.report.filter( Report.date <= end_date ).order_by( Report.date.desc() ).all()
							report_list = []
							for j in user_report:
								report_list.append( [ j.id, j.report, j.date.strftime("%d %b %Y") ] )
								reporting_count+=1

							reporting[ user.username ]=report_list
						else:
							return jsonify({ "returncode" : 1, "error" : "invalid date" })

				return jsonify({ "returncode" : 0, "reporting" : reporting, "msg" : [ "{} reporting fetched".format(reporting_count) ]  })

	return jsonify({ "returncode" : 1, "error" : "invalid data" })

	
@app.route("/delete_report", methods=["GET","POST"], endpoint="delete_report")
@login_required
@Admin						
def delete_report():
	if request.method=="POST" and request.is_json:
		data = request.get_json()
		msg=[]
		if ( "report_id_list" in data ):
			for id in data["report_id_list"]:
				report = Report.query.get( int(id) )
				if report:
					msg.append( "{}. {}'s reporting: {} has been deleted Successfully".format(report.id, report.user_obj.username, report.report) )
					db.session.delete(report)
					db.session.commit()
				else:
					return jsonify({ "returncode" : 1, "error" : "invalid id" })

			return jsonify({ "returncode" : 0, "msg" : msg }) 

	return jsonify({ "returncode" : 1, "error" : "invalid data" })

