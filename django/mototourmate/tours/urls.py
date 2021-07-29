from django.urls import path, include

from .views import  TourCreateView


urlpatterns = [
    path('create-tour/', TourCreateView.as_view()),
]