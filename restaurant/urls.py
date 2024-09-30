from django.urls import path
from django.conf import settings
from . import views

# URL paths for restaurant
urlpatterns = [
  path(r'', views.main, name = "main"), #homepage goes to main
  path(r'main', views.main, name = "main"), #main page of Zeno's
  path(r'order', views.order, name = "order"), #order page for food
  path(r'confirmation', views.confirmation, name = "confirmation"), #order confirmation page
]