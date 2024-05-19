from flask import Flask , render_template , request , redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from config import *
from flask_security import UserMixin, RoleMixin

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)
# db.init_app(app)
app.app_context().push()

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255),nullable=False)
    profile_pic = db.Column(db.String,nullable=False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    blogs = db.relationship('Blog',backref='owner')
    last_visited = db.Column(db.String,nullable=True)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Blog(db.Model):
    blog_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    title = db.Column(db.String,nullable=False)
    description = db.Column(db.String,nullable=False)
    content = db.Column(db.String,nullable=False)
    image = db.Column(db.String,nullable=False)
    time_stamp = db.Column(db.String,nullable=False)
    ref_user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

class Follwer(db.Model):
    network_id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    network_x = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    network_y = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)