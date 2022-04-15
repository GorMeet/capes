from django.urls import path
from django.views.generic import TemplateView
from .views import AddMailView

urlpatterns = [
    path("", AddMailView.as_view(), name="schedule"),
]
