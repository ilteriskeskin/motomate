from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import TourForm, LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linuxdegilgnulinux'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/alperen/proje/mototourmate/src/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


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


@app.route('/')
def home():
    tours = TourPost.query.all()
    return render_template('home.html', tours=tours)



@app.route('/tour-detail/<int:id>', methods=['GET'])
def tour_detail(id):
    tour_detail = User.query.filter_by(id=id).first()
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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash("Login is success!", "success")

                session['logged_in'] = True
                session['email'] = user.email

                return redirect(url_for('home'))
            else:
                flash("Wrong email or password", "danger")
                return redirect(url_for('login'))

    return render_template('auth/login.html', form=form)


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
    db.create_all()
    app.run(debug=True)
