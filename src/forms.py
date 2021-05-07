from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired


class TourForm(Form):
    name = StringField("Full Name", validators=[validators.Length(
        min=3, max=40), validators.DataRequired(message="Please fill this field")])
    email = StringField("Email", validators=[validators.Email(
        message="Enter a real email address"), validators.DataRequired(message="Please fill this field")])
    twitter_username = StringField("Twitter username")
    instagram_username = StringField("Instagram username")
    telegram_username = StringField("Telegram username")
    from_city = StringField("From City", validators=[
                            validators.DataRequired(message="Please fill this field")])
    to_city = StringField("To City", validators=[
                          validators.DataRequired(message="Please fill this field")])
    motorcycle_brand = StringField("Motorcycle brand", validators=[
                                   validators.DataRequired(message="Please fill this field")])
    engine_capacity = StringField("Engine Capacity (125cc)", validators=[
                                  validators.DataRequired(message="Please fill this field")])
    tour_date = StringField("Tour Date", validators=[
                       validators.DataRequired(message="Please fill this field")])
    note = TextAreaField("Note", validators=[validators.Length(max=240)])


class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(
        min=7, max=50), validators.DataRequired(message="Please fill this field")])
    password = PasswordField("Password", validators=[
                             validators.DataRequired(message="Please fill this field")])


class RegisterForm(Form):
    name = StringField("Full Name", validators=[validators.Length(
        min=3, max=25), validators.DataRequired(message="Please fill this field")])
    username = StringField("Username", validators=[validators.Length(
        min=3, max=25), validators.DataRequired(message="Please fill this field")])
    email = StringField("Email", validators=[validators.Email(
        message="Enter a real email address")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please fill this field"),
        validators.EqualTo(fieldname="confirm",
                           message="Your passwords do not match")
    ])
    confirm = PasswordField("Verify password", validators=[
                            validators.DataRequired(message="Please fill this field")])
