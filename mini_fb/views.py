from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
  '''Class for showing a profile'''
  model = Profile
  template_name = "mini_fb/show_profile.html"
  context_object_name = 'p'


class CreateProfileView(CreateView):
    '''View for creating a profile'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"


    def form_valid(self, form):
      '''Cleans data and adds it to the database on sucessful submission'''
      profile = form.save() 
      return super().form_valid(form)


    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.
        Sends user to profile they created'''
        return reverse('profile', kwargs={'pk': self.object.pk})
    

class CreateStatusMessageForm(CreateView):
    '''Class for creating status messages for profiles'''
    form_class = CreateStatusForm
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
      '''Cleans data and adds it to the database on sucessful submission'''
      print(form.cleaned_data)
      profile = Profile.objects.get(pk=self.kwargs['pk']) #gets primary key for the profile
      form.instance.profile = profile

      sm = form.save()
      files = self.request.FILES.getlist('files')

      for file in files:
         image = Image()
         image.statusMessage = sm
         image.image = file
         image.save()

      return super().form_valid(form)
    
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.
        Sends user to profile were they created the status'''
        return reverse('profile', kwargs={'pk': self.kwargs['pk']})
    

class UpdateProfileView(UpdateView):
    '''View for creating a profile'''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile
    context_object_name = 'p'

    def form_valid(self, form):
      '''Cleans data and adds it to the database on sucessful submission'''
      profile = form.save() 
      return super().form_valid(form)


    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.
        Sends user to profile they created'''
        return reverse('profile', kwargs={'pk': self.object.pk})
    
class DeleteStatusMessageView(DeleteView):
   model = StatusMessage
   template_name = "mini_fb/delete_status_form.html"
   context_object_name = "sm"

   def get_success_url(self) -> str:
    return reverse('profile', kwargs={'pk': self.object.profile.pk})
   
class UpdateStatusMessageView(UpdateView):
   form_class = UpdateStatusMessageForm
   model = StatusMessage
   template_name = "mini_fb/update_status_form.html"

   context_object_name = 'sm'

   def form_valid(self, form):
      sm = form.save() 
      return super().form_valid(form)
   
   def get_success_url(self) -> str:
      return reverse('profile', kwargs={'pk': self.object.profile.pk})