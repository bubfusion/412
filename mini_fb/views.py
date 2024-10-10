from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import *


# classed based view

class ShowAllView(ListView):
  '''Class for the /mini_fb page that shows all users'''
  model = Profile
  template_name = 'mini_fb/show_all_profiles.html'
  context_object_name = 'profiles'

class ShowProfilePageView(DetailView):
  model = Profile
  template_name = "mini_fb/show_profile.html"
  context_object_name = 'p'