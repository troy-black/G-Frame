import os

from gframe.json import Json

config = Json(__file__)

if config.get('SECRET_KEY') is None:
    config.data['SECRET_KEY'] = os.urandom(24).hex()

config.save()
