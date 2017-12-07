import re
from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        all__vary_rounds=0.1,
        pbkdf2_sha256__default_rounds=8000
)


def email_is_valid(email):
    address = re.compile('^[\w\d.+-]+@([\w\d.]+\.)+[\w]+$')
    return True if address.match(email) else False


def hash_password(password):
    return pwd_context.encrypt(password)


def check_hashed_password(password, hashed):
    return pwd_context.verify(password, hashed)