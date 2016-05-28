SETUP:
1) cd ~/Documents
2) git clone https://github.com/ladia12/bucketlistapi

Setup Virtual Environment and install flask
3) cd bucketlistapi
4) sudo pip install virtualenv
5) virtualenv venv
6) . venv/bin/activate
7) pip install Flask

Get all libraries used
8)pip install psycopg2==2.6.1 Flask-SQLAlchemy===2.1 Flask-Migrate==1.8.0 passlib==1.6.5 MySQL-python==1.2.5
9) pip freeze > requirements.txt

Setup DataBase:
10) Create database "bucketlist" with root username and no password
11) python bucketlist.py db init
12) python bucketlist.py db migrate

When any update in the migration file is done the use this command,
13) python bucketlist.py db upgrade

To run server
14) python bucketlist.py runserver