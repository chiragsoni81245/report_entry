import socket
import requests
import json
import os
from datetime import datetime
import sys

headers={'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Mobile Safari/537.36'}

base_address = "http://127.0.0.1:5000"
system = ["windows","linux"][os.name!="nt"]

root_username = sys.argv[1]
root_password = sys.argv[2]

def print_msg( msg ):
	clear_screen()

	if msg:
		for i in msg:		
			print( "** {} **".format(i) ) 
		input("\n\nPress Enter")


def clear_screen():
	if system=="linux":
		os.system("clear")
	else:
		os.system("cls")


def check_internet():
	while(1):
		try:
			check_response = json.loads( requests.get( base_address + "/check_server" ).text )
		except:
			check_response = False

		if check_response==False or check_response['returncode']!=0:
			print("No Internet Connection! or Server Can't Rechable")
			option = input("\n\nWana Retry? Yes[y] No[n] :")
			if option!="" and option[0].lower()=="n":
				exit()
		else:
			print("************ Internet Connected ***************")
			return True

		clear_screen()


def login( session, username, password ):

	check_internet()

	data = { "username" : username, "password" : password }

	response = session.post( base_address + "/login_page",data=data,headers=headers)	

	try:
		json_response = json.loads( response.text )
	except:
		print("Login Failed!!")
		exit()

	if int( json_response["returncode"] )==0:
		for i in json_response['msg']:
			print( i )
	else:
		print( json_response['error'] )
		exit()


def create_user( session, username, password ):
	
	check_internet()
	data = { "username" : username, "password": password } 
	response = session.post( base_address+"/register", data=data, headers=headers )

	try:
		response = json.loads( response.text )
	except:
		clear_screen()
		print("\nError in API")
		input("\n\nPress Enter")
		return None
	
	if response["returncode"]==0:
		return response['msg']
	else:
		clear_screen()
		print( response['error'] )
		input("\n\nPress Enter")
		return None


def submit_report( session, report ):
	
	check_internet()
	data = { "report" : report }
	response = session.post( base_address + "/add_report", json=data, headers=headers )

	try:
		response = json.loads( response.text )
	except:
		clear_screen()
		print("\nError in API")
		input("\n\nPress Enter")
		return None

	if response['returncode']==0:
		return response['msg']
	else:
		clear_screen()
		print( response['error'] )
		input("\n\nPress Enter")
		return None


def create_role( session, username, role_no ):

	check_internet()
	
	data = { "username" : username, "role_no" : role_no }

	response = session.post( base_address + "/add_role", json=data, headers=headers )

	try:
		response = json.loads( response.text )
	except:
		clear_screen()
		print("\nError in API")
		input("\n\nPress Enter")
		return None

	if response["returncode"]==0:
		return response['msg']
	else:
		clear_screen()
		print( response['error'] )
		input("\n\nPress Enter")
		return None


def fetch_user( session ):

	check_internet()
	
	response = session.get( base_address + "/fetch_user", headers=headers )

	try:
		response = json.loads( response.text )
	except:
		clear_screen()
		print("\nError in API")
		input("\n\nPress Enter")
		return None

	if response['returncode']==0:
		return response
	else:
		clear_screen()
		print( response['error'] )
		input("\n\nPress Enter")
		return None


def fetch_reporting( session, user_list, _filter_ ):

	check_internet()
	
	data = { "user_list" : user_list, "filter" : _filter_ }
	response = session.post( base_address + "/fetch_reporting", json=data, headers=headers )

	try:
		response = json.loads( response.text )
	except:
		clear_screen()
		print("\nError in API")
		input("\n\nPress Enter")
		return None

	if response['returncode']==0:
		return response
	else:
		clear_screen()
		print( response['error'] )
		input("\n\nPress Enter")
		return None


def fetch_reporting_caller( session ):
	
	no_of_user = input("\nNumber of User ( type ALL for all users ):")
	user_list = []
	_filter_ = {}

	if no_of_user.isnumeric():
		no_of_user = int(no_of_user)
		for i in range(no_of_user):
			user_list.append( input("\nEnter username:") )
	elif no_of_user=="ALL":
		user_list = fetch_user( s )['user_list']
	else:
		clear_screen()
		print("Invalid no. of users")
		input("\nPress Enter")
		return None

	option = input("\nFilter By Date Yes[y] No[n]:")
	if option!="" and option[0].lower()=="y":
		start_date = input("\nIf you wana ignore start date just press enter\n Enter Start Date in format (YYYY-MM-DD):")
		end_date = input("\nIf you wana ignore end date just press enter\n Enter end Date in format (YYYY-MM-DD):")
		
		_filter_['date']=[ start_date, end_date ]

	return fetch_reporting( session, user_list, _filter_ )


def display_reporting( reporting ):

	clear_screen()
	for user in reporting:
		print(user, end="\n\n")
		if len(reporting[user])==0:
			print(" \t No Reporting!")
		for id,report,date in reporting[user]:
			print('id: \033[31m{}\033[0m.\t{}  \033[32m"{}\033[0m"'.format(id,date,report))

		print("\n"+"-"*40, end="\n\n")

	input("\nPress Enter")


def delete_report( session, report_id_list ):
	
	check_internet()
	
	data = { "report_id_list" : report_id_list }

	response = session.post( base_address + "/delete_report", json=data, headers=headers )

	try:
		response = json.loads( response.text )
	except:
		clear_screen()
		print("\nError in API")
		input("\n\nPress Enter")
		return None

	if response['returncode']==0:
		return response
	else:
		clear_screen()
		print( response['error'] )
		input("\n\nPress Enter")
		return None


with requests.Session() as s:
	
	login( s, username=root_username,password=root_password )

	while (1):

		print("\n1: Add User\n2: Submit Report\n3: Submit Team Reportings\n4: Add Role\n5: Fetch Reporting\n6: Delete Report\n7: Exit")
	
		ch = input("Enter your choice:")

		clear_screen()

		if ch=="1":
			username = input("\nEnter Username:")
			password = input("\nEnter Password:")
			msg = create_user( s, username, password )
			print_msg( msg )

		elif ch=="2":
			count = int ( input("\nNo. of Reports You wana Enter:") )

			if count.isnumeric():
				count = int(count)
			else:
				clear_screen()
				print("Invalid no. of reports")
				input("\nPress Enter")
				continue

			report = []
			flag=0
			for i in range(count):
				d={}
				d["username"] = input("\nEnter Username:")
				d["report"] = input("\nEnter Report:")
				option = input("\nUse today's Date Yes[y] or No[n]:")
				if option!="" and option[0].lower()=="n":
					d["date"] = input("\nEnter Date in format(YYYY-MM-DD):")
				elif option=="" or option[0].lower()=="y":
					d["date"] = datetime.now().strftime("%Y-%m-%d")
				else:
					clear_screen()
					print("\nInvalid input!")
					input("\nPress Enter")
					flag=1
					break
				report.append(d)
			
			if flag==0:
				msg = submit_report( s, report )
				print_msg( msg )

		elif ch=="3":
			team = fetch_user( s )['user_list']
			report = []
			flag=0
			for i in team:
				d={ "username" : i }
				print("\n\t\t{}".format(i))
				d["report"] = input("\nEnter Report:")
				option = input("\nUse today's Date Yes[y] or No[n]:")
				if option!="" and option[0].lower()=="n":
					d["date"] = input("\nEnter Date in format(YYYY-MM-DD):")
				elif option=="" or option[0].lower()=="y":
					d["date"] = datetime.now().strftime("%Y-%m-%d")
				else:
					clear_screen()
					print("\nInvalid input!")
					input("\nPress Enter")
					flag=1
					break
				report.append(d)
			
			if flag==0:
				msg = submit_report( s, report )
				print_msg( msg )

		elif ch=="4":
			username = input("\nEnter Username:")
			role_no = input("\nRole Number:")
			msg = create_role( s, username, role_no )
			print_msg( msg )

		elif ch=="5":
			response_data = fetch_reporting_caller( s )
			if response_data:
				print_msg( response_data['msg'] )
				display_reporting( response_data['reporting'] )

		elif ch=="6":
			response_data = fetch_reporting_caller( s )
			if response_data:
				display_reporting( response_data['reporting'] )

			report_id = input("\nEnter id of reporting which you wana delete\n\nif they are multiple write them with a saperation of space\n:>>")
			report_id = report_id.split()
			report_id_list = []
			for i in report_id:
				if i.isnumeric():
					report_id_list.append( int(i) )
				else:
					break

			if len(report_id)==len(report_id_list):
				response_data = delete_report( s, report_id_list )
				if response_data:
					print_msg( response_data['msg'] )

			else:
				clear_screen()
				print("Invalid id")
				input("\nPress Enter")

		elif ch=="7":
			break
		else:
			print("Invalid Input") 

		clear_screen()
