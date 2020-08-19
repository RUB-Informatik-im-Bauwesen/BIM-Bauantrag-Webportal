from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app import db
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Integer, Table, Column, ForeignKey

user_roles_table = Table('user_roles_table', db.metadata,
                         Column('user_id', Integer, ForeignKey("users.id")),
                         Column('role_id', Integer, ForeignKey("roles.id"))
                         )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    firstName = db.Column(db.String(128))
    name = db.Column(db.String(128), index=True)
    password_hash = db.Column(db.String(128))
    activeRole = db.Column(db.String(128))
    assignedRoles = relationship("Role", secondary=user_roles_table)

    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(128), unique=True, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
