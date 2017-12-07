import random

import config
from db import db
from common.base_error import Error
from utils.security import hash_password, check_hashed_password
from models.games.games_players import GamePlayers


class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=False)
    remote_game = db.Column(db.Boolean, default=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', foreign_keys=[owner_id])

    associated = db.relationship('GamePlayers', back_populates='game')

    def __init__(self, name, owner, owner_plays, remote_game=False):
        self.name = name
        self.owner_id = owner.id
        self.players_assigned = False
        self.remote_game = remote_game
        if owner_plays:
            self.associated.append(GamePlayers(user_id=owner.id))

    def start(self):
        if len(self.associated) <= 2:
            raise Error('games-not_enough_players')
        if self.remote_game and not all([user.address for user in self.associated]):
            raise Error('games-not_all_players_with_address')
        for association in self.associated:
            other_players = {a.user_id for a in self.associated if a.user_id != association.user_id and a.friend_id != association.user_id}
            friend_ids = {a.friend_id for a in self.associated}
            available_players = other_players - friend_ids
            association.friend_id = available_players.pop()
            association.save_to_db()
        self.players_assigned = True

    def add_player(self, player):
        self.associated.append(GamePlayers(user_id=player.id))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
