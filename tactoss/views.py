from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *



class ShowHome(TemplateView):
  '''Class for the /tactoss page that shows the homepage'''
  template_name = 'tactoss/home.html'
  
class ShowAccountPageView(DetailView):
  '''Class for showing a profile'''
  model = Account
  template_name = "tactoss/show_account.html"
  context_object_name = 'account'

class ShowTeamPageView(DetailView):
  '''Class for showing a team'''
  model = Team
  template_name = "tactoss/show_team.html"
  context_object_name = 'team'

class ShowTeamsView(ListView):
  '''Class for showing all open teams'''
  model = Team
  template_name = "tactoss/teams.html"
  context_object_name = 'teams'
  
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