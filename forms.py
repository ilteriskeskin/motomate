from wtforms import Form, StringField, validators, TextAreaField


class TourForm(Form):
    tour_name = StringField("Tour Title")
    from_city = StringField("From City", validators=[
        validators.DataRequired(message="Please fill this field")])
    to_city = StringField("To City", validators=[
        validators.DataRequired(message="Please fill this field")])
    tour_date = StringField("Tour Date", validators=[
        validators.DataRequired(message="Please fill this field")])
    note = TextAreaField("Note", validators=[validators.Length(max=240)])


class ProfileForm(Form):
    twitter_username = StringField("Twitter username")
    instagram_username = StringField("Instagram username")
    telegram_username = StringField("Telegram username")
    city = StringField("City")
    motorcycle_brand = StringField("Motorcycle brand")
    engine_capacity = StringField("Engine Capacity (125cc)")
