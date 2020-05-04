# report_entry
this will help you to record your team reporting so that you can track your whole team growth 

![CLI Preview](/preview_image/Capture1.PNG)

**Steps To start Work on it**:

Linux User use:
  pip3 instead of pip
  python3 instead of python

1. Create a Virtualenv with: 
    1. install Virtualvenv ```pip install virtualenv```
    2. make a virtualenv with ```python -m virtualenv venv```
    3. activate virtualenv with:  goto venv directory with cmd, **Linux** : ```source bin/activate```, **Windows** : ```Script/activate```  
    4. install requrements: goto project root directory, ```pip install -r requrements.txt```
    
2. Setup database( run all these command in root directory of project ):
    1. To setup database ```flask db init```, ```flask db migrate```, ```flask db upgrade``` ( run all three of these commands respectivly )
    2. to create root user ```python database_initiation_script.py``` **(MUST)**
    
3. start API server( run all these command in root directory of project ):
    **( everytime you run API server you have to run this 2 command )**
    1. for Windows : ```set FLASK_APP=run.py```, for Linux : ```export FLASK_APP=run.py``` 
    2. to run API server ```flask run```
    
Control API with CLI_script:
    1. goto CLI directory in project 
    2. run CLI script ```python CLI_script_to_access_report_entry_api.py root_username root_password```
    
    ** Thats it now you can start intrating with api on  your local PC **
