from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from .models import Tour

class TourCreateView(CreateView):
    # template_name = "tours/create-tour.html"
    model = Tour
    fields = [
        "tour_name",
        "from_city",
        "to_city",
        "tour_date",
        "note"
    ]
