import flask
import json
import logging

from google.oauth2.credentials import Credentials as Google_Credentials

from gframe.json import Json


class Credentials(Json):
    def clear_credentials(self):
        logging.debug('Clearing Google API Credentials')
        if 'credentials' in flask.session:
            del flask.session['credentials']
        self.remove_local_file()

    def set_session_credentials(self, google_credentials: Google_Credentials):
        logging.debug('Setting Google API Session Credentials')
        session_credentials = {'token': google_credentials.token,
                               'refresh_token': google_credentials.refresh_token,
                               'token_uri': google_credentials.token_uri,
                               'client_id': google_credentials.client_id,
                               'client_secret': google_credentials.client_secret,
                               'scopes': google_credentials.scopes}
        flask.session['credentials'] = session_credentials
        self.data = json.loads(json.dumps(session_credentials))
        self.save()

    def save_data(self, google_credentials: Google_Credentials):
        self.set_session_credentials(google_credentials)


credentials = Credentials(__name__, load=False)
