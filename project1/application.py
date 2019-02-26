import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

# Instantiate Flask
app = Flask(__name__)

# Check for Auth0 client secret
if not os.getenv("AUTH0_SECRET"):
    raise RuntimeError("AUTH0_SECRET is not set.")
else:
    AUTH0_SECRET = os.getenv("AUTH0_SECRET")


# Set up Auth0
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='xSZQVTDHqPGkg2mpW8UBaVQ8uca3mu0V',
    client_secret=AUTH0_SECRET,
    api_base_url='https://bbhart1.auth0.com',
    access_token_url='https://bbhart1.auth0.com/oauth/token',
    authorize_url='https://bbhart1.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated
  
      


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:5000/callback', audience='https://bbhart1.auth0.com/userinfo')

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'xSZQVTDHqPGkg2mpW8UBaVQ8uca3mu0V'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    