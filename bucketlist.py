from flask import jsonify, abort, make_response, request, g
from models.models import *
from models.shared import db, create_app
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_httpauth import HTTPBasicAuth
from models import models
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = create_app()
file_handler = RotatingFileHandler('flask_app.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
                                    '[in %(pathname)s:%(lineno)d]'))
app.logger.addHandler(file_handler)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
auth = HTTPBasicAuth()


def _make_context():
    return dict(app=app, db=db, models=models)


manager.add_command('debug', Server(host="127.0.0.1", port=5000, use_debugger=True, use_reloader=True))
manager.add_command("shell", Shell(make_context=_make_context))


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


def generate_auth_token(user, expiration=31536000):
    s = Serializer(app.config['SECRET'], expires_in=expiration)
    return s.dumps({'id': user.id})


def verify_auth_token(token):
    serialized = Serializer(app.config['SECRET'])
    try:
        data = serialized.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    if data['id']:
        user = User.query.get(data['id'])
        return user
    return None


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(email=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    if email is None or password is None:
        abort(400)
    user = User.query.filter_by(email=email).first()
    if user is not None and (user.email == email and user.verify_password(password)):
        return jsonify({'success': True}), 201
    else:
        return jsonify({'invalid_user': True, 'user_logged_in': False}), 404


@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    password = request.json.get('password')
    contact_no = request.json.get("contact_no")
    email = request.json.get('email')
    if first_name is None or last_name is None or password is None or contact_no is None or email is None:
        abort(400)  # missing arguments
    else:
        user = User.query.filter_by(email=email).first()

        if user is not None:
            return jsonify({'user_exists': True, 'user_logged_in': False, 'email': user.email})
        # if user is not registered
        else:
            user = User(email=email)
            user.first_name = first_name
            user.last_name = last_name
            user.contact_number = contact_no
            user.hash_password(password)
            user.token = ""
            user.created_at = datetime.now()
            user.updated_at = datetime.now()
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=user.email).first()
            user.token = generate_auth_token(user).decode('ascii')
            db.session.commit()
            return jsonify({'success': True, 'token': user.token}), 201


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'email': user.email})


@app.route('/resource', methods=['GET'])
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello!'})


@app.route('/')
def hello():
    return "Yo! BuckList API is up"


if __name__ == '__main__':
    manager.run()
