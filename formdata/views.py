from django.shortcuts import render

# Create your views here.
def formdata(request):
  '''Fucntion to handle the URL request for /hw (home page)'''
  
  # template for home page
  template_name = "formdata/form.html"

  return render(request, template_name)