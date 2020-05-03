from app.models import *

root_user = input("\nEnter Root Username:") 
root_password = input("\nEnter Root Password:") 

root_user = User(username=username)
root_user.set_password(password)

db.session.add(root_user)
db.session.commit()
print("*** Root User {} Created ***".format(username))

user_id = User.query.filter_by(username=username).first().id
role = RoleManager(user=user_id,role_no=200)
db.session.add(root_user)
db.session.commit()

print("*** Role {} has been assigned to Root User {} ***".format(role.role_no, username))

