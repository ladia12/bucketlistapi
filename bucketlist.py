from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from models import models
from models.shared import db, create_app
from flask.ext.script import Manager,Server,Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.route('/')
def hello():
    return "Yo! BuckList API is up"

if __name__ == '__main__':
    manager.run()