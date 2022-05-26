import os

class InvalidEnvironVariableError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "INVALID ENV_VAR: "+self.msg

DATABASE = {
    "HOST": os.environ.get('DATABASE_HOST'),
    "DATABASE": os.environ.get('DATABASE'),
    "USER": os.environ.get('DATABASE_USER'),
    "PORT": "5432",
    "PASSWORD": os.environ.get('DATABASE_PASSWORD')
}

if None in DATABASE.values():
    raise InvalidEnvironVariableError(list(DATABASE.keys)[list(DATABASE.values).index(None)])