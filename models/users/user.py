import random

import config
from db import db
from common.base_error import Error
from utils.security import hash_password, check_hashed_password, email_is_valid
from models.users.user_invites import UserInvite


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(), unique=False)
    name = db.Column(db.String(255), unique=False)

    games_owned = db.relationship('Game')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.friend_id = None

    @property
    def address(self):
        return None

    def is_admin(self):
        return self.email in config.ADMINS

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def login(cls, email, password):
        user = cls.query.filter(User.email == email.lower()).first()

        if not user:
            raise Error('auth-email_not_found')

        if not check_hashed_password(password, user.password):
            raise Error('auth-incorrect_details')

        return user

    @classmethod
    def register(cls, name, email, password):
        user = cls(name,
                   email.lower(),
                   hash_password(password))
        user.save_to_db()
        return user

    def invite(self, email, game_id):
        if not email_is_valid(email):
            raise Error('error-email_invalid', email=email)
        invite = UserInvite(email, game_id=game_id)
        invite.save_to_db()
        invite.send(inviter_name=self.name)

