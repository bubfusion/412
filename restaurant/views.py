import random
import datetime
import pytz
from django.shortcuts import render
from django.utils import timezone



specials = [
  "Fried clams",
  "Haddock sandwich",
  "Shrimp"
]

prices = {
   "turkey" : 8,
   "fries" : 4,
   "beef" : 11,
   "special" : 12,
   "mayo": 0.50,
   "cheese" : 0.25,
   "sauce" : 0.25
}

items = [
  "turkey",
  "fries",
  "beef",
  "special",
  "mayo",
  "cheese",
  "sauce"
]

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
  
  # template for quotes page
  template_name = "restaurant/main.html"

  return render(request, template_name)

def order(request):
  '''Fucntion to handle the URL request for /main (restaurant's page)'''
  
  # template for quotes page
  template_name = "restaurant/order.html"

  context = {
    "special" : random.choice(specials)
  }

  return render(request, template_name, context)

def confirmation(request):
  '''Fucntion to handle the URL request for /main (restaurant's page)'''
  
  # template for quotes page
  template_name = "restaurant/confirmation.html"

  total = 0
  reciept = []

  # https://www.geeksforgeeks.org/how-to-add-time-onto-a-datetime-object-in-python/
  current_time = datetime.datetime.now()
  time_change = datetime.timedelta(minutes=random.randint(30,60)) 
  ready_time = current_time + time_change

  print(current_time)

  if request.POST:
        name = request.POST['name']
        for item in items:
           if item in request.POST:
              price = prices.get(item)
              total += price
              reciept.append(items_to_output.get(item))
              

        context = {
            'name': name,
            'total' : total,
            "reciept" : reciept,
            "ready_time" : ready_time
        }
  return render(request, template_name, context)