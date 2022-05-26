import os

class InvalidEnvironVariableError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "INVALID ENV_VAR: "+self.msg

bot_token = os.environ.get('BOTTOKEN')

if bot_token is None:
    raise InvalidEnvironVariableError('BOTTOKEN')

DATABASE = {
    "DATABASE_HOST": os.environ.get('DATABASE_HOST'),
    "DATABASE": os.environ.get('DATABASE'),
    "DATABASE_USER": os.environ.get('DATABASE_USER'),
    "DATABASE_PORT": "5432",
    "DATABASE_PASSWORD": os.environ.get('DATABASE_PASSWORD')
}

if None in DATABASE.values():
    raise InvalidEnvironVariableError(list(DATABASE.keys)[list(DATABASE.values).index(None)])