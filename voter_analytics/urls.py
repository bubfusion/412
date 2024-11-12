from django.urls import path
from django.conf import settings
from . import views

# URL paths for mini_fb
urlpatterns = [
  path(r'', views.ShowAllView.as_view(), name = "voters"), 
]