from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .models import *
from .forms import *
from .forms import CreateProfileForm


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


class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def form_valid(self, form):
      print(form.cleaned_data)
      profile = form.save() 
      return super().form_valid(form)

## also:  revise the get_success_url
    def get_success_url(self) -> str:
        print(self.kwargs)
        '''Return the URL to redirect to after successfully submitting form.'''
        return reverse('profile', kwargs={'pk': self.object.pk})