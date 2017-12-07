from tests.base_test import BaseTest

from models.users.user import User
from models.games.game import Game


class TestGame(BaseTest):
    def test_create_game(self):
        user = User('Test User', 'test@test.com', '1234')
        game = Game('Test Game', user, True)

        self.assertTrue(game.associated[0].user_id == user.id)

    def test_add_players(self):
        users = [
            User('Test User', 'test@test.com', '1234'),
            User('Test User 2', 'test2@test.com', '1234'),
            User('Test User 3', 'test3@test.com', '1234'),
        ]
        game = Game('Test Game', users[0], True)

        for user in users[1:]:
            game.add_player(user)

        for user in users:
            self.assertIn(user.id, (assoc.user_id for assoc in game.associated))

    def test_start_game(self):
        users = [
            User('Test User', 'test@test.com', '1234'),
            User('Test User 2', 'test2@test.com', '1234'),
            User('Test User 3', 'test3@test.com', '1234'),
        ]

        with self.app_context():
            [u.save_to_db() for u in users]
            game = Game('Test Game', users[0], True)

            for user in users[1:]:
                game.add_player(user)

            game.save_to_db()

            game.start()

            self.assertTrue(game.players_assigned)

            for user in users:
                self.assertIn(user.id, (assoc.friend_id for assoc in game.associated))
