from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.shortcuts import redirect



class ShowHome(TemplateView):
  '''Class for the /tactoss page that shows the homepage'''
  template_name = 'tactoss/home.html'
  
class ShowAccountPageView(DetailView):
  '''Class for showing a profile'''
  model = Account
  template_name = "tactoss/show_account.html"
  context_object_name = 'account'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # Check if the user is authenticated
    if self.request.user.is_authenticated:
        account = Account.objects.filter(user=self.request.user).first()
        context['account_logged'] = account
        
    return context

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
    # Check if the user is authenticated
    if self.request.user.is_authenticated:
        account = Account.objects.filter(user=self.request.user).first()
        context['account'] = account
        
    return context
  
class JoinTeamView(LoginRequiredMixin, View):
  '''View for joining a team'''
  def dispatch(self, request, *args, **kwargs):
    account = Account.objects.filter(user=self.request.user).first()
    team = Team.objects.filter(pk=kwargs['pk']).first()
    if account.user_team == None and team.slot_open():
      print("success")
      team.add_player(account)
      account.save()
      team.save()
    empty_slot = False
    for player in [team.team_leader, team.account_2, team.account_3, team.account_4, team.account_5]:
      if player == None:
        empty_slot = True
        break
    if empty_slot == False:
      team.is_open = False
    
    team.save()
      
    return redirect('team', pk=team.pk)
  
class CreateTeam(LoginRequiredMixin, View):
  def dispatch(self, request, *args, **kwargs):
    account = Account.objects.filter(user=self.request.user).first()
    if account.user_team == None:
      team = Team.objects.create(team_leader=account, is_open=True)
      account.user_team = team
      account.save()
      return redirect('team', pk=team.pk)
    else:
      return redirect('teams')

class LeaveTeam(LoginRequiredMixin, View):
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
              team.is_open = True
              team.save()
      return redirect('teams')
  
# Friend system inspired by https://medium.com/analytics-vidhya/add-friends-with-689a2fa4e41d
class SendFriendRequest(LoginRequiredMixin, View):
  def dispatch(self, request, *args, **kwargs):
    from_account = Account.objects.filter(user=self.request.user).first()
    to_account = Account.objects.filter(user=kwargs['request_pk']).first()
    print(from_account)
    print(to_account)
    
    if from_account != to_account:
      friend_request, new = Friend_Requests.objects.get_or_create(
        from_account=from_account, to_account = to_account)
    return redirect('friends')

class AcceptFriendRequest(LoginRequiredMixin, View):
  def dispatch(self, request, *args, **kwargs):
    friend_request = Friend_Requests.objects.get(pk=kwargs['request_pk'])
    if friend_request.to_account.user == self.request.user:
      friend_request.to_account.friends.add(friend_request.from_account)
      friend_request.from_account.friends.add(friend_request.to_account)
      friend_request.delete()
    return redirect('friends')
  
class CancelFriendRequest(LoginRequiredMixin, View):
  def dispatch(self, request, *args, **kwargs):
    friend_request = Friend_Requests.objects.get(pk=kwargs['request_pk'])
    if friend_request.from_account.user == self.request.user:
      friend_request.delete()
    return redirect('friends')

class DeclineFriendRequest(LoginRequiredMixin, View):
  def dispatch(self, request, *args, **kwargs):
    friend_request = Friend_Requests.objects.get(pk=kwargs['request_pk'])
    if friend_request.to_account.user == self.request.user:
      friend_request.delete()
    return redirect('friends')

class FriendStatus(LoginRequiredMixin, DetailView):
  model = Account
  template_name = "tactoss/friends.html"
  context_object_name = 'account'
  
  def get_object(self):
    '''Returns the logged in user object'''
    return Account.objects.get(user=self.request.user)

class CreateAccountView(CreateView):
  '''View for creating a profile'''
  form_class = CreateAccountForm
  template_name = "tactoss/create_account_form.html"


  def form_valid(self, form):
    '''Cleans data and adds it to the database on sucessful submission'''
    
    # gets instance of account form
    user_creation_form = UserCreationForm(self.request.POST)
    user = user_creation_form.save()
    account = form.instance
    
    # Sets fk to newly created user
    account.user = user
    account_picture = self.request.FILES.get('account_picture')
    if account_picture != None:
      account.account_picture = account_picture
    account.save()
    # Logs user in after making account
    login(self.request, user) 
    
    return redirect(self.get_success_url())


  def get_success_url(self) -> str:
      '''Return the URL to redirect to after successfully submitting form.
      Sends user to profile they created'''
      return reverse('home')
    
  def get_context_data(self, **kwargs):
    '''Gets the context for user creation form'''
    context = super().get_context_data(**kwargs)
    user_creation_form = UserCreationForm()
    context['user_creation_form'] = user_creation_form
    return context
  

class ShowFeedView(ListView):
  '''Class for showing all open teams'''
  model = SmokeGif
  template_name = "tactoss/feed.html"
  context_object_name = 'lineups'
  ordering = ['-published']

class CreateLineuptView(CreateView):
  '''View for creating a profile'''
  form_class = CreateLineupForm
  template_name = "tactoss/create_lineup_form.html"


  def form_valid(self, form):
    '''Cleans data and adds it to the database on sucessful submission'''
    
    # gets instance of account form
    lineup = form.instance
    
    # Sets fk to newly created user
    lineup.account = Account.objects.filter(user=self.request.user).first()
    print(Account.objects.filter(user=self.request.user).first())
    
    gif = self.request.FILES.get('gif')
    if gif != None:
      lineup.gif = gif
    lineup.save()
  
    return redirect(self.get_success_url())


  def get_success_url(self) -> str:
      '''Return the URL to redirect to after successfully submitting form.
      Sends user to profile they created'''
      return reverse('feed')
    
class UpdateAccounteView(LoginRequiredMixin, UpdateView):
    '''View for updating a profile'''
    form_class = UpdateAccountForm
    template_name = "tactoss/update_account_form.html"
    model = Account
    context_object_name = 'account'

    def form_valid(self, form):
      '''Cleans data and updates it in the database on sucessful submission'''
      account = form.save()
      
      account_picture = self.request.FILES.get('account_picture')
      if account_picture != None:
        account.account_picture = account_picture
      account.save()
      
      return super().form_valid(form)
    
    def get_object(self):
      '''Returns the logged in user object'''
      return Account.objects.get(user=self.request.user)


    def get_success_url(self) -> str:
        '''Return the URL to the profile that was updated'''
        return reverse('account', kwargs={'pk': self.object.pk})