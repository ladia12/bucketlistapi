

> SETUP


    cd ~/Documents
    git clone https://github.com/ladia12/bucketlistapi

**Setup Virtual Environment and install flask**

    cd bucketlistapi
    sudo pip install virtualenv
    virtualenv venv
    . venv/bin/activate
    pip install Flask

**Get all libraries used**

    pip install psycopg2==2.6.1 Flask-SQLAlchemy===2.1 Flask-Migrate==1.8.0 passlib==1.6.5 MySQL-python==1.2.5
    
    pip freeze > requirements.txt

**Setup DataBase**
Create database "bucketlist" with root username and no password

    python bucketlist.py db init
    python bucketlist.py db migrate

**When any update in the migration file is done the use this command**

    python bucketlist.py db upgrade

**To run server**

    python bucketlist.py runserver