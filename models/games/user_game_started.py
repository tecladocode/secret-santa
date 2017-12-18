from flask import url_for, request

from libs.mailgun import Mailgun


def send_user_game_started_notification(email, name, friend_name, game_name):
    return Mailgun.send_email(email,
                              subject_key='game-your_secret_santa',
                              text_key='game-secret_santa_text',
                              name=name,
                              friend_name=friend_name,
                              game_name=game_name,
                              link=request.url_root[:-1] + url_for('game', name=game_name))
