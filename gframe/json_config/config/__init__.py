import os
from pathlib import Path

from gframe.json_config import Json


config = Json(__name__)

if config.get('SECRET_KEY') is None:
    config.data['SECRET_KEY'] = os.urandom(24).hex()

if config.get('DOWNLOAD_PHOTO_PATH') is None:
    config.data['DOWNLOAD_PHOTO_PATH'] = os.path.join(
            config.get_local_path(), 'Photos'
    )

path = config.get('DOWNLOAD_PHOTO_PATH')
if '~' in path:
    config.data['DOWNLOAD_PHOTO_PATH'] = path.replace('~', str(Path.home()))

config.save()
