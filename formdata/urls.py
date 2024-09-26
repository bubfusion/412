from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
  path(r'', views.formdata, name = "formdata"),
  path(r'submit', views.submit, name = "submit")
]