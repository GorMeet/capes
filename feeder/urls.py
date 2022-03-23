from django.urls import path
from django.views.generic import TemplateView
from .views import home, fetchfeed

urlpatterns = [
        path('', home, name="home"),
        path('feed/', fetchfeed, name="fetchfeed"), 
        ]
