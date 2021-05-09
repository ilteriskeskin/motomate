from mototourmate.users.models import BaseModel
from .cities import Cities


class TourForm(BaseModel):
    from_city = models.CharField(max_length=20, choices=Cities.choices,)

    to_city = StringField("To City", validators=[
                          validators.DataRequired(message="Please fill this field")])
    tour_date = StringField("Tour Date", validators=[
                       validators.DataRequired(message="Please fill this field")])
    description = TextAreaField("Note", validators=[validators.Length(max=240)])