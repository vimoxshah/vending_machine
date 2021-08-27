
### Vending Machine

- system must have python3.7, postgres running on 5432 port


- Steps to run the project in local

- clone this repo
- create vritual env using `virtualenv -p python3.7 venv`
- now you can activate it using `source activate venv/bin/activate`
- you can load env variables using `source local_export.sh`

- install the requirements using `pip3 install -r vending_machine/requirements.txt`

- create database name `vending_machine_development`

- now run the db migrations using `python3 manage.py migrate` - this will add tables

- there is one file of Postman collection name in this repo Vending Machine.postman_collection.json. Import this to your Postman it has all the apis.

- you can now start the server using command `gunicorn -c gconf.py vending_machine.wsgi`


Features

- APIs
    - create user
    - update user
    - delete user
    - get user
    - login
    - logout
    - deposit
    - reset deposit
    - create product
    - update product
    - delete product
    - get product
    - buy product

- Global level common HTTP exception
- Token based authentication
- gunicorn configured server
- configured server logs

## How to Test apis?

- assuming you have server up and running on port 8000. you can test apis from given postman collection. apart from create user all apis require authentication token that you have to pass in header
Authorization Token <token> . you can first login using login api by giving username, password you will get token in response that will be valid for 24hrs. now you can use that token in all other api.
- you can run test cases using `python3 manage.py test`
