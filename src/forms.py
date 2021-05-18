from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField, DateField


class TourForm(Form):
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