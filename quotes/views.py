from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random
import time


# List of Jerry quotes
quote_list = ["Constantly choosing the lesser of two evils is still choosing evil.", "What a long strange trip it has been",
              "Ah shit, I spilled chocolate milkshake all over my favorite sweatpants"]

#List of photos of Jerry
photo_list = ["https://www.metrowestdailynews.com/gcdn/authoring/2008/04/24/NMWD/ghows-WL-6c391fdf-f53d-4634-be73-613f1d3d993d-7a753d5a.jpeg?width=1200&disable=upscale&format=pjpg&auto=webp",
              "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Jerry-Garcia-01cropped.jpg/640px-Jerry-Garcia-01cropped.jpg",
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQUYFAf6lKulaq_pkMCq3Pyj1H1D0-V4USwow&s"]

def quotes(request):
  '''Fucntion to handle the URL request for /quotes (quotes page)'''
  
  # template for quotes page
  template_name = "quotes/quote.html"

  # Passes list for a random photo and quote to context
  context = {
    "displayed_quote" : random.choice(quote_list),
    "displayed_photo" : random.choice(photo_list)
  }

  return render(request, template_name, context)

def show_all(request):
  '''Fucntion to handle the URL request for /show_all (show all page with all
  quotes and photos)'''

  # Render template for show all page
  template_name = "quotes/show_all.html"

  # Passes list for all photos and quotes to context
  context = {
    "all_quotes" : quote_list,
    "all_photos" : photo_list
  }

  return render(request, template_name, context)

def about(request):
  '''Fucntion to handle the URL request for /about (about section for Jerry)'''

  # Render template for about page
  template_name = "quotes/about.html"

  return render(request, template_name)