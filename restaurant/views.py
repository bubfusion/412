import random
import datetime
import pytz
from django.shortcuts import render
from django.utils import timezone


# Offering for seafood special
specials = [
  "Fried clams",
  "Haddock sandwich",
  "Shrimp"
]

# Dictionary for prices for each item
prices = {
   "turkey" : 8,
   "fries" : 4,
   "beef" : 11,
   "special" : 12,
   "mayo": 0.50,
   "cheese" : 0.25,
   "sauce" : 0.25
}

# Array of all items
items = [
  "turkey",
  "fries",
  "beef",
  "special",
  "mayo",
  "cheese",
  "sauce"
]

# Way to get presentable name from name of html element for food items
items_to_output = {
   "turkey" : "Turkey sub",
   "fries" : "French fries",
   "beef" : "Super beef",
   "mayo": "Mayo",
   "cheese" : "Cheese",
   "sauce" : "Sauce",
   "special" : "Seafood special",
}


def main(request):
  '''Fucntion to handle the URL request for /main (restaurant's page)'''
  
  # template for main page
  template_name = "restaurant/main.html"

  return render(request, template_name)

def order(request):
  '''Fucntion to handle the URL request for /order (food ordering page)'''
  
  # template for order page
  template_name = "restaurant/order.html"

  # Generates random special from the list
  context = {
    "special" : random.choice(specials)
  }

# returns with template and special
  return render(request, template_name, context)

def confirmation(request):
  '''Fucntion to handle the URL request for /confirmation (confirmation page for order)'''
  
  # template for confirmation page
  template_name = "restaurant/confirmation.html"

  # Keeps track of total price
  total = 0
  # Keeps track of items ordered
  reciept = []

  # used this source to help me learn how to add time to datetime object 
  # https://www.geeksforgeeks.org/how-to-add-time-onto-a-datetime-object-in-python/
  current_time = datetime.datetime.now()
  time_change = datetime.timedelta(minutes=random.randint(30,60)) 
  ready_time = current_time + time_change

  # Checks to make sure the request is post
  if request.POST:
        # Sets user's name
        name = request.POST['name']
        # loops through items to find what items were purchased
        # also sums all of the prices of the items bought
        for item in items:
           if item in request.POST:
              price = prices.get(item)
              total += price
              reciept.append(items_to_output.get(item))
              

        # passes context for the confirmation page
        context = {
            'name': name,
            'total' : total,
            "reciept" : reciept,
            "ready_time" : ready_time
        }

  # returns
  return render(request, template_name, context)