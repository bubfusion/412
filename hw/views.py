from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
# Create your views here.

def home(request):
  '''Fucntion to handle the URL request for /hw (home page)'''
  
  # template for home page
  template_name = "hw/home.html"

  # dic of context vars for template

  context = {
    "current_time" : time.ctime,
  }
  return render(request, template_name, context)