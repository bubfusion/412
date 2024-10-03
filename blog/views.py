from django.shortcuts import render

from django.views.generic import ListView
from .models import *


# classed based view

class ShowAllView(ListView):
  model = Article
  template_name = 'blog/show_all.html'
  context_object_name = 'articles'