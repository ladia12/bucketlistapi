from shared import db
from sqlalchemy import *
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32))
    password_hash = db.Column(db.String(120))
    token = db.Column(db.String(130), nullable=False)
    email = db.Column(db.String(130), nullable=False, unique=True)
    contact_number = db.Column(db.String(12))
    profile_url = db.Column(db.String(130))
    about_me = db.Column(db.Text)
    city = db.Column(db.String(32))
    country = db.Column(db.String(32))
    no_goals_added = db.Column(db.Integer)
    no_goals_completed = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    user_goals = db.relationship('UserGoal', backref="user", cascade="all, delete-orphan", lazy='dynamic')
    ug_likes = db.relationship('UserGoalLike', backref=db.backref('user', lazy='joined'), lazy='dynamic',
                               cascade="all, delete, delete-orphan")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Goal(db.Model):
    __tablename__ = 'goal'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    image_url = db.Column(db.String(130))
    no_added = db.Column(db.Integer)
    no_completed = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    user_goals = db.relationship('UserGoal', backref="goal", cascade="all, delete-orphan", lazy='dynamic')


class UserGoal(db.Model):
    __tablename__ = 'usergoal'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    likes = db.Column(db.Integer, default=0)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    date_target = db.Column(db.DateTime)
    privacy = db.Column(db.SmallInteger)
    list_id = db.Column(db.ForeignKey('list.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    ug_likes = db.relationship('UserGoalLike', backref=db.backref('usergoal', lazy='joined'), lazy='dynamic',
                               cascade="all, delete, delete-orphan")


class UserGoalLike(db.Model):
    __tablename__ = "user_goal_like"
    id = db.Column(db.Integer, primary_key=True)
    user_goal_id = db.Column(db.ForeignKey('usergoal.id'))
    user_id = db.Column(db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


association_table = Table('association', db.Model.metadata,
                          Column('goal_id', Integer, ForeignKey('goal.id')),
                          Column('category_id', Integer, ForeignKey('category.id'))
                          )


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    goal = db.relationship("Goal",
                           secondary=association_table,
                           backref="categories")


class List(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'))
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    goals = db.relationship('UserGoal', backref="list", lazy='dynamic')


class SuccessStory(db.Model):
    __tablename__ = "successstory"
    id = db.Column(db.Integer, primary_key=True)
    user_goal_id = db.Column(db.ForeignKey('usergoal.id'))
    story = db.Column(db.Text)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    date_completed = db.Column(db.DateTime)
    likes = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(130))
    video_url = db.Column(db.String(130))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    ss_likes = db.relationship('SuccessStoryLike', backref=db.backref('successstory', lazy='joined'), lazy='dynamic',
                               cascade="all, delete, delete-orphan")


class SuccessStoryLike(db.Model):
    __tablename__ = "success_story_like"
    id = db.Column(db.Integer, primary_key=True)
    success_story_id = db.Column(db.ForeignKey('successstory.id'))
    user_id = db.Column(db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
