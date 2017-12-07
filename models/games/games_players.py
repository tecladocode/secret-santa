from db import db

class GamePlayers(db.Model):
    __tablename__ = 'players'

    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), primary_key=True)
    game = db.relationship('Game', back_populates='', foreign_keys=[game_id])
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user = db.relationship('User', back_populates='', foreign_keys=[user_id],
    	backref=db.backref('associated', lazy=True))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend = db.relationship('User', foreign_keys=[friend_id])

    def save_to_db(self):
    	db.session.add(self)
    	db.session.commit()
  