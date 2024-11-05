from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse
from .models import *
from .forms import *
from .forms import CreateProfileForm
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

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
      
      # gets instance of account form
      user_creation_form = UserCreationForm(self.request.POST)
      user = user_creation_form.save()
      profile = form.instance
      
      # Sets fk to newly created user
      profile.user = user
      
      # Logs user in after making account
      login(self.request, user) 
      
      return super().form_valid(form)


    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.
        Sends user to profile they created'''
        return reverse('profile', kwargs={'pk': self.object.pk})
      
    def get_context_data(self, **kwargs):
      '''Gets the context for user creation form'''
      context = super().get_context_data(**kwargs)
      user_creation_form = UserCreationForm()
      context['user_creation_form'] = user_creation_form
      return context
    

class CreateStatusMessageForm(LoginRequiredMixin, CreateView):
    '''Class for creating status messages for profiles'''
    form_class = CreateStatusForm
    template_name = "mini_fb/create_status_form.html"

    def form_valid(self, form):
      '''Cleans data and adds it to the database on sucessful submission'''
      print(form.cleaned_data)
      profile = Profile.objects.get(user=self.request.user) #gets primary key for the profile
      form.instance.profile = profile
      sm = form.save() #saves text


      files = self.request.FILES.getlist('files') #gets image files from form
      for file in files:
        #  loops through all the images and adds them to the DB
         image = Image()
         image.statusMessage = sm
         image.image = file
         image.save()

      return super().form_valid(form)
    
    
    def get_object(self):
      '''Returns the logged in user object'''
      return Profile.objects.get(user=self.request.user)
    
    def get_success_url(self) -> str:
      '''Returns URL for the profile that the status message is on'''
      return reverse('profile', kwargs={'pk': self.object.profile.pk})
      
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''View for updating a profile'''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile
    context_object_name = 'p'

    def form_valid(self, form):
      '''Cleans data and updates it in the database on sucessful submission'''
      profile = form.save() 
      return super().form_valid(form)
    
    def get_object(self):
      '''Returns the logged in user object'''
      return Profile.objects.get(user=self.request.user)


    def get_success_url(self) -> str:
        '''Return the URL to the profile that was updated'''
        return reverse('profile', kwargs={'pk': self.object.pk})
    
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
   '''View for deleting a status message'''
   model = StatusMessage
   template_name = "mini_fb/delete_status_form.html"
   context_object_name = "sm"

   def get_success_url(self) -> str:
    '''Returns URL back to the profile that the status was on'''
    return reverse('profile', kwargs={'pk': self.object.profile.pk})
   
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
   '''View for updating a status message'''
   form_class = UpdateStatusMessageForm
   model = StatusMessage
   template_name = "mini_fb/update_status_form.html"
   context_object_name = 'sm'

   def form_valid(self, form):
      '''Function for saving status message to DB if form is valid'''
      sm = form.save() 
      return super().form_valid(form)
   
   def get_success_url(self) -> str:
      '''Returns URL for the profile that the status message is on'''
      return reverse('profile', kwargs={'pk': self.object.profile.pk})

class CreateFriendView(LoginRequiredMixin, View):
  '''View for adding friends'''
  def dispatch(self, request, *args, **kwargs):
    profile1 = Profile.objects.filter(user=self.request.user).first()
    profile2 = Profile.objects.filter(pk=kwargs['other_pk']).first()
    profile1.add_friend(profile2)
    #Couldn't get reverse to work so I used this as a work around
    return redirect('profile', pk=profile1.pk)
  
  def get_object(self):
    '''Returns the logged in user object'''
    return Profile.objects.get(user=self.request.user)
  
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
  '''View for suggesting friends'''
  model = Profile
  template_name = "mini_fb/friend_suggestions.html"
  context_object_name = 'p'
  
  def get_object(self):
    '''Returns the logged in user object'''
    return Profile.objects.get(user=self.request.user)

  
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
  '''View for showing a newsfeed of a profile'''
  model = Profile
  template_name = "mini_fb/news_feed.html"
  context_object_name = 'p'
  
  def get_object(self):
    '''Returns the logged in user object'''
    return Profile.objects.get(user=self.request.user)
