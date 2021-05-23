import os
import json

from flask import Flask, render_template, flash, redirect, request, session, url_for
import flask
from forms import TourForm, ProfileForm
from functools import wraps

# Google Authentication

from oauthlib.oauth2 import WebApplicationClient
import requests
from bson import ObjectId

from utils.database import db

GOOGLE_CLIENT_ID = "1034191173571-nrf1kvoenfab8ca52r2tpl3k3nqocal0.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "GhRyXEqcV_pJw4QkpL8dbknt"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linuxdegilgnulinux'
db.init()

client = WebApplicationClient(GOOGLE_CLIENT_ID)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def home():
    tours = db.find('tours', {})
    tours_array = []
    for tour in tours:
        tours_array.append(tour)
    return render_template('home.html', tours=tours_array)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/user/<email>')
def user_detail(email):
    user = db.find_one('users', {"email": email})
    return render_template('user-detail.html', user=user)


@app.route('/profile')
@login_required
def profile():
    user = db.find_one('users', {"email": session['email']})
    return render_template('profile.html', user=user)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = db.find_one('users', {"email": session['email']})
    form = ProfileForm(request.form)
    if request.method == 'GET':
        form['twitter_username'].data = user.get('twitter_username')
        form['instagram_username'].data = user.get('instagram_username')
        form['telegram_username'].data = user.get('telegram_username')
        form['city'].data = user.get('city')
        form['motorcycle_brand'].data = user.get('motorcycle_brand')
        form['engine_capacity'].data = user.get('engine_capacity')

    elif request.method == 'POST' and form.validate:
        db.find_and_modify('users', query={'email': session['email']},
                           twitter_username=form.twitter_username.data,
                           instagram_username=form.instagram_username.data,
                           telegram_username=form.telegram_username.data,
                           city=form.city.data.lower(),
                           motorcycle_brand=form.motorcycle_brand.data,
                           engine_capacity=form.engine_capacity.data.lower().replace(' ', ''),
                           )

        flash('Profile Updated!', 'success')
        return redirect(url_for('profile'))
    return render_template('edit-profile.html', form=form)


@app.route('/edit-tour/<id>', methods=['GET', 'POST'])
@login_required
def edit_tour(id):
    tour = db.find_one('tours', {"_id": ObjectId(id)})
    if session['email'] == tour['email']:
        form = TourForm(request.form)
        if request.method == 'GET':
            form['tour_name'].data = tour.get('tour_name')
            form['from_city'].data = tour.get('from_city')
            form['to_city'].data = tour.get('to_city')
            form['tour_date'].data = tour.get('tour_date')
            form['note'].data = tour.get('note')

        elif request.method == 'POST' and form.validate:
            db.find_and_modify('tours', query={'_id': ObjectId(id)},
                               tour_name=form.tour_name.data,
                               from_city=form.from_city.data,
                               to_city=form.to_city.data,
                               tour_date=form.tour_date.data.lower(),
                               note=form.note.data,
                               )

            flash('Tur Bilgileri Güncellendi!', 'success')
            return redirect(url_for('home'))
        return render_template('edit-tour.html', form=form, id=tour['_id'])
    else:
        flash('Yalnızca kendi turlarını düzenleyebilirsin!', 'danger')
        return redirect(url_for('home'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get("q")
    query = query.lower()
    tours = db.find('tours', {'from_city': query})
    tours_array = []
    for tour in tours:
        tours_array.append(tour)
    return render_template('search-result.html', tours=tours_array)


@app.route('/tour-detail/<id>', methods=['GET'])
def tour_detail(id):
    tour_details = db.find_one('tours', {
        '_id': ObjectId(id)
    })
    return render_template('tour-detail.html', tour_detail=tour_details)


@app.route('/create-tour/', methods=['GET', 'POST'])
@login_required
def create_tour():
    form = TourForm(request.form)
    if request.method == 'POST' and form.validate:
        tour_id = db.insert_one('tours', {
            'tour_name': form.tour_name.data,
            'name': session['name'],
            'email': session['email'],
            'from_city': form.from_city.data.lower(),
            'to_city': form.to_city.data.lower(),
            'tour_date': form.tour_date.data,
            'note': form.note.data,
            'subscriber': [session['email']]
        })

        user = db.find_one("users", {'email': session['email']})
        user['joined_tours'].append(
            {"id": ObjectId(tour_id.inserted_id), "tour_name": form.tour_name.data, })
        db.find_and_modify(
            'users', query={'email': session['email']}, joined_tours=user['joined_tours'])

        flash('New tour created!', 'success')
        return redirect(url_for('home'))

    return render_template('create-tour.html', form=form)


@app.route('/join-tour/<id>', methods=['POST'])
@login_required
def join_tour(id):
    tour = db.find_one("tours", {'_id': ObjectId(id)})
    user = db.find_one("users", {'email': session['email']})
    if session['email'] not in tour['subscriber']:
        tour['subscriber'].append(session['email'])
        user['joined_tours'].append(
            {"id": ObjectId(id), "tour_name": tour['tour_name']})

        db.find_and_modify("tours", query={"_id": ObjectId(
            id)}, subscriber=tour['subscriber'])
        db.find_and_modify(
            'users', query={'email': session['email']}, joined_tours=user['joined_tours'])

        flash('Tura katıldın!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Zaten bu tura katılıyorsun!', 'warning')
        return redirect(url_for('home'))


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
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        session['logged_in'] = True
        session['email'] = users_email
        session['name'] = users_name
        flash("Login is success!", "success")

        user = db.find_one('users', {
            'email': users_email
        })
        if not user:
            db.insert_one("users", {
                'email': users_email,
                'name': users_name,
                'picture': picture,
                'joined_tours': [],
            })
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
