import logging
import os
import shutil

import flask
import google.oauth2.credentials
import googleapiclient.discovery
import requests

from gframe.json.credentials import credentials
from gframe.json.config import config


def sync_google_photos():
    logging.debug('Google Photos Sync Starting')
    try:
        logging.debug('Setting Session Credentials')
        session_credentials = google.oauth2.credentials.Credentials(
                **flask.session['credentials'])

        logging.debug('Building Google Photos API')
        photos_api = googleapiclient.discovery.build(
                config.get('API_SERVICE_NAME'),
                config.get('API_VERSION'),
                cache_discovery=False,
                credentials=session_credentials,
        )

        album_dict = photos_api.albums().list().execute()
        logging.debug('Reading Google Albums')

        sync_albums(album_dict['albums'], photos_api)
        credentials.save_data(session_credentials)
        logging.debug('Google Photos Sync Complete')

    except Exception as e:
        logging.critical('Failed to Sync Google Photos', e)
        return False
    return True


def sync_albums(albums: dict, photos_api):
    for album in albums:
        logging.debug('Reading Google Album: ' + album['title'])
        if album_in_sync_list(album['title']):
            logging.debug('Syncing Google Album: ' + album['title'])
            body = {"albumId": album['id']}
            media_dict = photos_api.mediaItems().search(body=body).execute()
            path = os.path.join(
                    config.get('DOWNLOAD_PHOTO_PATH'),
                    album['title'],
            )
            verify_path_exists(path)
            sync_media(media_dict['mediaItems'], path)
    remove_old_albums(
            os.listdir(config.get('DOWNLOAD_PHOTO_PATH')),
            [t['title'] for t in albums],
    )


def album_in_sync_list(album_name: str) -> bool:
    return any({True for album in config.get('ALBUM_SYNC_LIST')
                if album == album_name
                or ('*' in album and album.replace('*', '') in album_name)})


def verify_path_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def sync_media(media_files: list, path: str):
    remove_old_files([f['filename'] for f in media_files], path)
    for media in media_files:
        file_name = os.path.join(path, media['filename'])
        if config.get('API_FORCE_MEDIA_UPDATE') or not os.path.isfile(
                file_name):
            if media['mimeType'].startswith('video'):
                media_url = media['baseUrl'] + config.get(
                    'API_DOWNLOAD_VIDEO_EXTENSION')
            else:
                media_url = media['baseUrl'] + config.get(
                    'API_MAX_RESOLUTION_EXTENSION')
            download_media(media_url, file_name)


def download_media(media_url: str, file_name: str):
    logging.debug('Downloading: ' + media_url)
    media_response = requests.get(media_url)
    if media_response.status_code == 200:
        save_file(file_name, media_response.content)
    else:
        logging.warning('Download Failed: ' + media_url)
        logging.warning('Status Code: ' + media_response.status_code)


def save_file(file_name: str, content: bytes):
    try:
        with open(file_name, 'wb') as file:
            file.write(content)
        logging.debug('File Saved: ' + file_name)
    except Exception as e:
        logging.critical('Save Failed: ' + file_name, e)


def remove_old_files(media_file_names: list, path: str):
    for remove_file in [file for file in os.listdir(path)
                        if file not in media_file_names]:
        file_name = os.path.join(path, remove_file)
        os.remove(file_name)
        logging.debug('Removed: ' + file_name)


def remove_old_albums(local_album_names: list, album_names: list):
    for remove_album in [path for path in local_album_names
                         if path not in album_names]:
        path = os.path.join(config.get('DOWNLOAD_PHOTO_PATH'), remove_album)
        shutil.rmtree(path)
        logging.debug('Removed Album: ' + path)
