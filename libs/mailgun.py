import requests

from utils.localisation import localise


class Mailgun:
    CONFIG = None

    @classmethod
    def initialize(cls, config):
        cls.CONFIG = config

    @classmethod
    def send_email(cls, email, subject, text):
        return requests.post(
            "https://api.mailgun.net/v3/{}/messages".format(cls.CONFIG.MAILGUN_DOMAIN),
            auth=("api", cls.CONFIG.MAILGUN_API_KEY),
            data={"from": "{} <santa@{}>".format(localise('email-title'), cls.CONFIG.MAILGUN_DOMAIN),
                  "to": [email],
                  "subject": subject,
                  "text": text})
