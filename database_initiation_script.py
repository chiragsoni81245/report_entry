from app.models import *

root_user = input("\nEnter Root root_user:") 
root_password = input("\nEnter Root Password:") 

user = User( username=root_user )
user.set_password( root_password )

db.session.add(root_user)
db.session.commit()
print("*** Root User {} Created ***".format(root_user))

user_id = User.query.filter_by(username=root_user).first().id
role = RoleManager(user=user_id,role_no=200)
db.session.add(role)
db.session.commit()

print("*** Role {} has been assigned to Root User {} ***".format(role.role_no, root_user))

