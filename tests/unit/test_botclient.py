from unittest import TestCase

from client_corleone.botclient import BotClient


class TestBotClient(TestCase):
    def test_token_in_url(self):
        token = 'SomeToken'
        botclient = BotClient(token)
        self.assertTrue(token in botclient.bot_url)
