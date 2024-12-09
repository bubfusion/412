from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
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
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    account = Account.objects.filter(user=self.request.user).first()
    context['account'] = account
    return context
  
class JoinTeamView(LoginRequiredMixin, View):
  '''View for joining a team'''
  def dispatch(self, request, *args, **kwargs):
    account = Account.objects.filter(user=self.request.user).first()
    print(account)
    team = Team.objects.filter(pk=kwargs['pk']).first()
    print(account)
    if account.user_team == None and team.slot_open():
      print("success")
      team.add_player(account)
      account.save()
    
    if team.slot_open() == False:
      team.slot_open = False
      team.save()
    return redirect('team', pk=team.pk)
  
class CreateTeam(View):
  def dispatch(self, request, *args, **kwargs):
    account = Account.objects.filter(user=self.request.user).first()
    if account.user_team == None:
      team = Team.objects.create(team_leader=account, is_open=True)
      account.user_team = team
      account.save()
      return redirect('team', pk=team.pk)
    else:
      return redirect('teams')

class LeaveTeam(View):
  def dispatch(self, request, *args, **kwargs):
    account = Account.objects.filter(user=self.request.user).first()
    team = account.user_team
    if team == None:
      return redirect('teams')
    else:
      if team.team_leader == account:
        team.delete()
      else:
        for player in [team.team_leader, team.account_2, team.account_3, team.account_4, team.account_5]:
          if account == player:
              print(player)
              account.user_team = None
              account.save()
              if account == team.team_leader:
                team.team_leader = None
              elif account == team.account_2:
                team.account_2 = None
              elif account == team.account_3:
                team.account_3 = None
              elif account == team.account_4:
                team.account_4 = None
              elif account == team.account_5:
                team.account_5 = None
              team.save()
      return redirect('teams')
  
