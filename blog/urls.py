from django.urls import path
from django.conf import settings
from . import views

# URL paths for restaurant
urlpatterns = [
  path(r'', views.ShowAllView.as_view(), name = "show_all"),
]