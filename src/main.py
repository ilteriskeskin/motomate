import os
import json

from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import TourForm, LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Google Authentication
from oauthlib.oauth2 import WebApplicationClient
import requests

GOOGLE_CLIENT_ID = "1034191173571-nrf1kvoenfab8ca52r2tpl3k3nqocal0.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GhRyXEqcV_pJw4QkpL8dbknt"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linuxdegilgnulinux'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///Users/burakyilmaz/Development/mototourmate/src/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(25))


class TourPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
    twitter_username = db.Column(db.String(80), unique=True)
    instagram_username = db.Column(db.String(80), unique=True)
    telegram_username = db.Column(db.String(80), unique=True)
    from_city = db.Column(db.String(80))
    to_city = db.Column(db.String(80))
    motorcycle_brand = db.Column(db.String(80))
    engine_capacity = db.Column(db.String(80))
    tour_date = db.Column(db.String(80))
    note = db.Column(db.String(80))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route('/')
def home():
    tours = TourPost.query.all()
    return render_template('home.html', tours=tours)


@app.route('/tour-detail/<int:id>', methods=['GET'])
def tour_detail(id):
    tour_detail = TourPost.query.filter_by(id=id).first()
    return render_template('tour-detail.html', tour_detail=tour_detail)


@app.route('/create-tour/', methods=['GET', 'POST'])
@login_required
def create_tour():
    form = TourForm(request.form)
    if request.method == 'POST' and form.validate:
        new_tour = TourPost(
            creator=session['email'],
            name=form.name.data,
            email=form.email.data,
            twitter_username=form.twitter_username.data,
            instagram_username=form.instagram_username.data,
            telegram_username=form.telegram_username.data,
            from_city=form.from_city.data.lower(),
            to_city=form.to_city.data.lower(),
            motorcycle_brand=form.motorcycle_brand.data,
            engine_capacity=form.engine_capacity.data.lower().replace(' ', ''),
            tour_date=form.tour_date.data,
            note=form.note.data
        )

        db.session.add(new_tour)
        db.session.commit()
        flash('New tour created!', 'success')
        return redirect(url_for('home'))

    return render_template('create-tour.html', form=form)


# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm(request.form)
#     if request.method == 'POST' and form.validate:
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             if check_password_hash(user.password, form.password.data):
#                 flash("Login is success!", "success")
#
#                 session['logged_in'] = True
#                 session['email'] = user.email
#
#                 return redirect(url_for('home'))
#             else:
#                 flash("Wrong email or password", "danger")
#                 return redirect(url_for('login'))
#
#     return render_template('auth/login.html', form=form)

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User(
        id=unique_id, name=users_name, email=users_email
    )
    return redirect(url_for('home'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        new_user = User(name=form.name.data, username=form.username.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered is success!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('auth/register.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    db.create_all()
    app.run(debug=True)
