from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

from django.shortcuts import redirect



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
  
class JoinTeamView(LoginRequiredMixin, View):
  '''View for joining a team'''
  def dispatch(self, request, *args, **kwargs):
    account = Account.objects.filter(user=self.request.user).first()
    print(account)
    team = Team.objects.filter(pk=kwargs['pk']).first()
    print(account)
    if team.in_team_already(account) == False and team.slot_open():
      print("success")
      team.add_player(account)
    
    if team.slot_open() == False:
      team.slot_open = False
      team.save()
    return redirect('team', pk=team.pk)
    
