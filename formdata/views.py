from django.shortcuts import render

# Create your views here.
def formdata(request):
  '''Fucntion to handle the URL request for /hw (home page)'''
  
  # template for home page
  template_name = "formdata/form.html"

  return render(request, template_name)


def submit(request):

  template_name = "formdata/confirmation.html"
  if request.POST:
        name = request.POST['name']
        color = request.POST['color']
        context = {
            'name': name,
            'color': color,
            
        }
  return render(request, template_name, context=context)