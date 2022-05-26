from .base import *
import os

class InvalidEnvNameException(Exception):
    def __str__(self):
        return "INVALID ENVIRONMENT NAME: "+str(os.environ.get("ENV_NAME"))

if os.environ.get("ENV_NAME") == "STAGE":
    from .stage import *
elif os.environ.get("ENV_NAME") == "PRODUCT":
    from .product import *
else:
    raise InvalidEnvNameException()

ENV_NAME = os.environ.get("ENV_NAME")