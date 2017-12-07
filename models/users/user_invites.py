import datetime
import uuid

import requests
from flask import url_for, request

from utils.localisation import localise
from db import db
import config


class UserInvite(db.Model):
    __tablename__ = 'invites'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String)
    email = db.Column(db.String)

    created_date = db.Column(db.DateTime)

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    game = db.relationship('Game')

    def __init__(self, email, game_id):
        self.email = email
        self.game_id = game_id
        self.created_date = datetime.datetime.utcnow()
        self.uuid = uuid.uuid4().hex

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def send(self, inviter_name):
        email_request = requests.post(
            "https://api.mailgun.net/v3/{}/messages".format(config.MAILGUN_DOMAIN),
            auth=("api", config.MAILGUN_API_KEY),
            data={"from": "{} <santa@{}>".format(localise('email-title'), config.MAILGUN_DOMAIN),
                  "to": [self.email],
                  "subject": localise('game-you_have_been_invited'),
                  "text": localise('game-invitation_text', inviter=inviter_name,
                                   link=request.url_root[:-1] + url_for('confirm_invite',
                                                                        confirmation_id=self.uuid))})
        return email_request
