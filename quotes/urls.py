from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
  path(r'', views.quotes, name = "quotes"),
  path(r'quotes', views.quotes, name = "quotes"),
  path(r'show_all', views.show_all, name = "show all"),
  path(r'about', views.about, name = "about"),
]