import os

from flask import Flask, session, request, render_template, g, redirect, url_for
from db import db

from libs.mailgun import Mailgun
from utils.localisation import localise
from common.base_error import Error
from models.users.user import User
from models.users.user_invites import UserInvite
from models.games.game import Game
from models.games.games_players import GamePlayers

import config


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.urandom(32)


@app.template_global(name='localise')
def localisation_filter(s, **kwargs):
    return localise(s, **kwargs)


@app.before_first_request
def init_db():
    get_db()
    Mailgun.initialize(config)


def get_db():
    db.create_all()


@app.errorhandler(Error)
def handle_app_error(e):
    return render_template('50x.jinja2', message=e.message)


@app.route('/')
def home():
    return render_template('home.jinja2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = User.login(email, password)
            session['user_id'] = user.id
        except Error as e:
            return render_template('login.jinja2', message=e.message)

        return redirect(url_for('profile'))

    if g.user:
        return redirect(url_for('profile'))

    return render_template('login.jinja2')


@app.route('/logout')
def logout():
    session['user_id'] = None
    session['confirmation_id'] = None
    return redirect(url_for('home', message=localise('site-logged_out')))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('profile', message=localise('site-already_logged_in')))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = User.register(name, email, password)
            session['user_id'] = user.id

            if session.get('confirmation_id'):
                conf = UserInvite.query.filter(UserInvite.uuid == session['confirmation_id']).first()
                conf.game.add_player(user)
                conf.game.save_to_db()
                session['confirmation_id'] = None

                return redirect(url_for('game', name=conf.game.name))
        except Error as e:
            return render_template('register.jinja2', message=e.message)

        return redirect(url_for('profile'))

    return render_template('register.jinja2')


@app.route('/profile')
def profile():
    if not g.user:
        return render_template('home.jinja2', message=localise('identity-need_logged_in'))
    return render_template('profile.jinja2', user=g.user)


@app.route('/playing')
def playing():
    return render_template('games.jinja2', games=g.user.games)


@app.route('/created')
def created():
    return render_template('created.jinja2', games=Games.query.filter(Game.owner_id == g.user.id))


@app.route('/game/<string:name>')
def game(name):
    return render_template('game.jinja2', game=Game.query.filter(Game.name == name).first())


@app.route('/start_game/<string:name>')
def start_game(name):
    game = Game.query.filter(Game.name == name).first()
    try:
        game.start()
    except Error as e:
        return redirect(url_for('game', name=name, message=e.message))
    return redirect(url_for('game', name=name))


@app.route('/game', methods=['GET', 'POST'])
def create_game():
    if request.method == 'POST':
        owner_plays = request.form.get('owner_plays', 'off') == 'on'
        name = request.form.get('name')
        try:
            Game(name, g.user, owner_plays).save_to_db()
            return redirect(url_for('game', name=name))
        except Exception as e:
            return redirect(url_for('create_game', message=localise('games-error_creating')))       
    return render_template('create_game.jinja2')


@app.route('/game/<string:name>/invite', methods=['GET', 'POST'])
def invite_player(name):
    game = Game.query.filter(Game.name == name).first()
    if not game:
        raise Error('games-game_doesnt_exist')

    if request.method == 'POST':
        email = request.form.get('email')

        g.user.invite(email, game.id)
    return render_template('invite.jinja2', game=game)


@app.route('/confirm_invite/<string:confirmation_id>')
def confirm_invite(confirmation_id):
    session['confirmation_id'] = confirmation_id
    return redirect(url_for('register', message=localise('game-register_to_join_game')))


@app.route('/admin')
def admin():
    if not g.user.is_admin():
        return render_template('home.jinja2', message=localise('access-dont_have_access'))
    return render_template('admin.jinja2')


@app.before_request
def before_request():
    """
    Pull user's profile from the database before every request is started.
    """
    g.user = None
    session['locale'] = request.args.get('locale', session.get('locale', 'en-GB'))
    g.locale = session['locale']
    if session.get('user_id'):
        g.user = User.query.get(session['user_id'])



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000)
