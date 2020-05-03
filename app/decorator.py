from flask_login import current_user


def Admin( function ):

	def check_admin(*args,**kwargs):
		if current_user.role.role_no>=200:
			return function(*args,**kwargs)

		return jsonify({ "returncode":1, "error":"Permission Denied" })

	return check_admin