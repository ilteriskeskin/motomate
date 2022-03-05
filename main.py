import os
import json

from flask import Flask, render_template, flash, redirect, request, session, url_for
from forms import TourForm, ProfileForm, GroupForm
from functools import wraps

# Google Authentication

from oauthlib.oauth2 import WebApplicationClient
import requests
from bson import ObjectId

from utils.group_name_diff import similar
from utils.database import db
from configs import SECRET_KEY, GOOGLE_CLIENT_SECRET, GOOGLE_CLIENT_ID

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
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
    tours = db.find('tours', {}).limit(10)
    groups = db.find('groups', {}).limit(10)

    tours_array = []
    group_array = []

    for tour in tours:
        tours_array.append(tour)

    for group in groups:
        group_array.append(group)

    return render_template('home.html', tours=tours_array, groups=group_array)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/tours')
def tours():
    tours = db.find('tours', {})
    return render_template('tours.html', tours=tours)


@app.route('/groups')
def groups():
    groups = db.find('groups', {})
    return render_template('groups.html', groups=groups)


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


@app.route('/search-group', methods=['GET', 'POST'])
def search_group():
    query = request.args.get("q")
    query = query.lower()
    groups = list(db.find('groups', {}))
    groups_array = []

    if groups:
        for group in groups:
            similar_rate = similar(query, group['group_name'].lower())
            print(similar_rate)
            if similar_rate > 0.37:
                groups_array.append(group)

    return render_template('search-result-for-groups.html', groups=groups_array)


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get("q")
    query = query.lower()
    tours = list(db.find('tours', {'from_city': query}))
    tours_array = []

    if tours:
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


@app.route('/edit-group/<id>', methods=['GET', 'POST'])
@login_required
def edit_group(id):
    group = db.find_one('groups', {"_id": ObjectId(id)})
    if session['email'] in group['admins']:
        form = GroupForm(request.form)
        if request.method == 'GET':
            form['group_name'].data = group.get('group_name')
            form['city'].data = group.get('city')
            form['email'].data = group.get('email')
            form['note'].data = group.get('note')

        elif request.method == 'POST' and form.validate:
            db.find_and_modify('groups', query={'_id': ObjectId(id)},
                               group_name=form.group_name.data,
                               city=form.city.data,
                               email=form.email.data,
                               note=form.note.data,
                               )

            flash('Grup Bilgileri Güncellendi!', 'success')
            return redirect(url_for('home'))
        return render_template('edit-group.html', form=form, id=group['_id'])
    else:
        flash('Yalnızca kendi turlarını düzenleyebilirsin!', 'danger')
        return redirect(url_for('home'))


@app.route('/group-detail/<id>', methods=['GET'])
def group_detail(id):
    group_details = db.find_one('groups', {
        '_id': ObjectId(id)
    })
    print(group_details)
    return render_template('group-detail.html', group_detail=group_details)


@app.route('/create-group/', methods=['GET', 'POST'])
@login_required
def create_group():
    form = GroupForm(request.form)
    if request.method == 'POST' and form.validate:
        group_id = db.insert_one('groups', {
            'group_name': form.group_name.data,
            'email': form.email.data,
            'city': form.city.data.lower(),
            'members': [session['email']],
            'note': form.note.data,
            'admins': [session['email']]
        }).inserted_id

        user = db.find_one("users", {'email': session['email']})
        if user.get('joined_groups'):
            user['joined_groups'].append(
                {"id": ObjectId(group_id), "group_name": form.group_name.data, })
        else:
            user['joined_groups'] = [{
                "id": ObjectId(group_id),
                "group_name": form.group_name.data
            }]
        db.find_and_modify(
            'users', query={'email': session['email']}, joined_groups=user['joined_groups'])

        flash('New group created!', 'success')
        return redirect(url_for('home'))

    return render_template('create-group.html', form=form)


@app.route('/join-group/<id>', methods=['POST'])
@login_required
def join_group(id):
    group = db.find_one("groups", {'_id': ObjectId(id)})
    user = db.find_one("users", {'email': session['email']})
    if session['email'] not in group['members']:
        group['members'].append(session['email'])
        user['joined_groups'].append(
            {"id": ObjectId(id), "group_name": tour['group_name']})

        db.find_and_modify("groups", query={"_id": ObjectId(
            id)}, members=group['members'])
        db.find_and_modify(
            'users', query={'email': session['email']}, joined_groups=user['joined_groups'])

        flash('Gruba katıldın!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Zaten bu gruptasın!', 'warning')
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
