from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import *



class ShowHome(TemplateView):
  '''Class for the /tactoss page that shows the homepage'''
  template_name = 'tactoss/home.html'