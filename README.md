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
8) pip freeze > requirements.txt

Setup DataBase:
9) Create database "bucketlist" with root username and no password
10) python bucketlist.py db init
11) python bucketlist.py db migrate

When any update in the migration file is done the use this command,
12) python bucketlist.py db upgrade

To run server
13) python bucketlist.py runserver