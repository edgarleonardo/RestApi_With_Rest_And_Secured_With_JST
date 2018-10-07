
# Rest API with Python using Flask

In this example shows a simple REST-CRUD  API using Flask microframework, sqlite for persistent the data and JWT for securing some endpoints.

To run this project you need Python 3 and pip.

Once we have Python up and running just head to the command interface and install the next package if are no installed already:

**pip install flask
pip install flask_sqlalchemy
pip install jwt**

Once the package installed just run:

**python app.py**

To Start testing the rest service.

In order to be able to login, you are going to create an user using the Python REPL:

**from userModel import *
User.createuser('admin','admin')**

Now just go to the login endpoint and get the Token using the user and passwords already created.
