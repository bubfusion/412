from django.urls import path
from django.conf import settings
from . import views

# URL paths for restaurant
urlpatterns = [
  path(r'', views.ShowHome.as_view(), name = "home")
]