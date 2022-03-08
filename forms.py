from wtforms import Form, StringField, validators, TextAreaField, BooleanField
from wtforms.fields.html5 import EmailField


class TourForm(Form):
    tour_name = StringField("Tour Title")
    from_city = StringField("From City", validators=[
        validators.DataRequired(message="Please fill this field")])
    to_city = StringField("To City", validators=[
        validators.DataRequired(message="Please fill this field")])
    tour_date = StringField("Tour Date", validators=[
        validators.DataRequired(message="Please fill this field")])
    note = TextAreaField("Note", validators=[validators.Length(max=240)])
    is_private = BooleanField("Gruba Özel mi?")


class ProfileForm(Form):
    twitter_username = StringField("Twitter username")
    instagram_username = StringField("Instagram username")
    telegram_username = StringField("Telegram username")
    city = StringField("City")
    motorcycle_brand = StringField("Motorcycle brand")
    engine_capacity = StringField("Engine Capacity (125cc)")


class GroupForm(Form):
    group_name = StringField("Group Name", validators=[
        validators.DataRequired(message="Please fill this field")])
    city = StringField("City", validators=[
                       validators.DataRequired(message="Please fill this field")])
    email = EmailField("Email", validators=[
                       validators.Email(message="Invalid email address")])
    note = TextAreaField("Note", validators=[validators.Length(max=240)])
