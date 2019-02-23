import os
import json
import time
import logging
import flask
import google.oauth2.credentials
import google_auth_oauthlib.flow
import mimetypes
import requests

from gframe.json.credentials import credentials
from gframe import google_photos
from gframe.local_media import Media
from gframe.json.config import config
from gframe.json.client_secret import client_secret

logging.debug('Setting Environment Variables')
# Disable HTTPS
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Relax Tokens
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = flask.Flask(__name__)
app.secret_key = config.get('SECRET_KEY')

# Force JSON to Return as Pretty/Readable Print
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

last_api_call = 0


@app.route('/')
def index():
    if not os.path.isfile(credentials.get_local_json_path()):
        logging.debug('Loading initial Setup GUI')
        return flask.render_template('setup.html')
    else:
        global last_api_call
        # Limit how often Google Photos API is called
        if time.time() - last_api_call >= config.get(
                'LIMIT_API_REFRESH_SECONDS'):
            # If Authorization is required, return Google OAuth2 Login
            if 'credentials' not in flask.session or not google_photos.sync_google_photos():
                return flask.redirect('authorize')
            last_api_call = int(time.time())
        return flask.render_template(
                'play.html',
                refresh=int(config.get('LIMIT_DISPLAY_REFRESH_MILLISECONDS')),
        )


@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret.get_local_json_path(),
            scopes=config.get('API_SERVICE_SCOPES'),
    )

    # The URI created here must exactly match one of the authorized redirect
    # URIs for the OAuth 2.0 client, which you configured in the API Console.
    # If this value doesn't match an authorized URI, you will get a
    # 'redirect_uri_mismatch' error.
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token
            # without re-prompting the user for permission. Recommended for
            # web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true',
    )

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            client_secret.get_local_json_path(),
            scopes=config.get('API_SERVICE_SCOPES'),
            state=state,
    )
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    credentials.save_data(flow.credentials)

    return flask.redirect('/')


@app.route('/revoke')
def revoke():
    if 'credentials' in flask.session:
        session_credentials = google.oauth2.credentials.Credentials(
                **flask.session['credentials']
        )
        requests.post(
                'https://accounts.google.com/o/oauth2/revoke',
                params={'token': session_credentials.token},
                headers={'content-type': 'application/x-www-form-urlencoded'},
        )
    return flask.redirect('/')


@app.route('/clear')
def clear():
    credentials.clear_credentials()
    return flask.redirect('/')


@app.route('/random')
def random_media_info():
    filename = Media().random_media(config.get('DOWNLOAD_PHOTO_PATH'))
    return flask.jsonify(**{
        'filename': filename,
        'mimetype': mimetypes.guess_type(filename)[0],
    })


@app.route('/media')
def get_media():
    filename = flask.request.args.get('filename', 'static/blank.jpg')
    return flask.send_file(filename, mimetype=mimetypes.guess_type(filename)[0])


@app.route('/json_config', methods=['PUT'])
def put_config():
    config.save_data(json.dumps(flask.request.json))
    return flask.jsonify(**config.data)


@app.route('/json_config', methods=['GET'])
def get_config():
    return flask.jsonify(**config.data)


@app.route('/config')
def view_config():
    return flask.render_template('config.html')


@app.route('/json_client_secret', methods=['PUT'])
def put_client_secret():
    client_secret.save_data(json.dumps(flask.request.json))
    return flask.jsonify(**client_secret.data)


@app.route('/json_client_secret', methods=['GET'])
def get_client_secret():
    return flask.jsonify(**client_secret.data)


@app.route('/client_secret')
def view_client_secret():
    return flask.render_template('client_secret.html')


@app.after_request
def add_header(response):
    # Disable caching
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    # Specify a hostname and port that are set as a valid redirect URI for
    # your API project in the Google API Console.
    app.run('localhost', 5000)
