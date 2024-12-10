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
    '''Gets context and adds current user to it'''
    context = super().get_context_data(**kwargs)
    # Check if the user is authenticated
    if self.request.user.is_authenticated:
        account = Account.objects.filter(user=self.request.user).first()
        # adds current logged in user to context. Used for checking if current
        # account being viewed is theirs and to check friend status
        context['account_logged'] = account
        
    return context

class ShowTeamPageView(DetailView):
  '''Class for showing a specific team'''
  model = Team
  template_name = "tactoss/show_team.html"
  context_object_name = 'team'

class ShowTeamsView(ListView):
  '''Class for showing all open teams'''
  model = Team
  template_name = "tactoss/teams.html"
  context_object_name = 'teams'
  
  def get_context_data(self, **kwargs):
    '''Gets and adds current logged in account to context'''
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
    
    # Checks if user isn't in a team already and if team has open slot
    if account.user_team == None and team.slot_open():
      # Adds player to a team and updates it
      team.add_player(account)
      account.save()
      team.save()
    # Variable to check if team has an open slot
    empty_slot = False
    # Loops through all player slots
    for player in [team.team_leader, team.account_2, team.account_3, team.account_4, team.account_5]:
    # If the current player slot is open, means team isn't full. Updates variable
      if player == None:
        empty_slot = True
        break
    # If team is full, updates its bool that keeps track of it
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
  '''Class for view to send request'''
  def dispatch(self, request, *args, **kwargs):
    '''Handles logic for adding friends'''
    from_account = Account.objects.filter(user=self.request.user).first()
    to_account = Account.objects.filter(user=kwargs['request_pk']).first()
    
    if from_account != to_account:
      # Only creates new if to player is not logged in player
      # and if they isn't an outbound request
      friend_request, new = Friend_Requests.objects.get_or_create(
        from_account=from_account, to_account = to_account)
    return redirect('friends')

class AcceptFriendRequest(LoginRequiredMixin, View):
  '''Class for view to accept friend request'''
  def dispatch(self, request, *args, **kwargs):
    '''Handles accepting logic'''
    friend_request = Friend_Requests.objects.get(pk=kwargs['request_pk'])
    # Check to make sure logged in user matches the recieving user
    if friend_request.to_account.user == self.request.user:
      friend_request.to_account.friends.add(friend_request.from_account)
      friend_request.from_account.friends.add(friend_request.to_account)
      # Deletes friend request object
      friend_request.delete()
    return redirect('friends')
  
class CancelFriendRequest(LoginRequiredMixin, View):
  '''View for cancelling a friend request (sender)'''
  def dispatch(self, request, *args, **kwargs):
    friend_request = Friend_Requests.objects.get(pk=kwargs['request_pk'])
    if friend_request.from_account.user == self.request.user:
      friend_request.delete()
    return redirect('friends')

class DeclineFriendRequest(LoginRequiredMixin, View):
  '''Class for declining a friend request (reciever)'''
  def dispatch(self, request, *args, **kwargs):
    friend_request = Friend_Requests.objects.get(pk=kwargs['request_pk'])
    if friend_request.to_account.user == self.request.user:
      friend_request.delete()
    return redirect('friends')

class FriendStatus(LoginRequiredMixin, DetailView):
  '''View to see friends of yours'''
  model = Account
  template_name = "tactoss/friends.html"
  context_object_name = 'account'
  
  def get_object(self):
    '''Returns the logged in account object'''
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
    # Checks if a profile image was uploaded (there is default if one is not)
    if account_picture != None:
      account.account_picture = account_picture
    account.save()
    # Logs user in after making account
    login(self.request, user) 
    
    return redirect(self.get_success_url())


  def get_success_url(self) -> str:
      '''Return the URL to redirect to after successfully submitting form.
      Sends user to home page'''
      return reverse('home')
    
  def get_context_data(self, **kwargs):
    '''Gets the context for user creation form'''
    context = super().get_context_data(**kwargs)
    user_creation_form = UserCreationForm()
    context['user_creation_form'] = user_creation_form
    return context
  

class ShowFeedView(ListView):
  '''Class for showing all lineup gifs'''
  model = SmokeGif
  template_name = "tactoss/feed.html"
  context_object_name = 'lineups'
  # Sorts by when they were added
  ordering = ['-published']

class CreateLineuptView(CreateView):
  '''View for creating a lineup gif'''
  form_class = CreateLineupForm
  template_name = "tactoss/create_lineup_form.html"


  def form_valid(self, form):
    '''Cleans data and adds it to the database on sucessful submission'''
    
    # gets instance of account form
    lineup = form.instance
    
    # Sets account fk to newly created lineup
    lineup.account = Account.objects.filter(user=self.request.user).first()
    print(Account.objects.filter(user=self.request.user).first())
    
    # Gets image from upload
    gif = self.request.FILES.get('gif')
    if gif != None:
      lineup.gif = gif
    lineup.save()
  
    return redirect(self.get_success_url())


  def get_success_url(self) -> str:
      '''Return the URL to redirect to after successfully submitting form.
      Sends user to the feed'''
      return reverse('feed')
    
class UpdateAccounteView(LoginRequiredMixin, UpdateView):
    '''View for updating an account'''
    form_class = UpdateAccountForm
    template_name = "tactoss/update_account_form.html"
    model = Account
    context_object_name = 'account'

    def form_valid(self, form):
      '''Cleans data and updates it in the database on sucessful submission'''
      account = form.save()
      
      # Checks if a new image was uploaded and applies it if so
      account_picture = self.request.FILES.get('account_picture')
      if account_picture != None:
        account.account_picture = account_picture
      account.save()
      
      return super().form_valid(form)
    
    def get_object(self):
      '''Returns the logged in user object'''
      return Account.objects.get(user=self.request.user)


    def get_success_url(self) -> str:
        '''Return the URL to the account that was updated'''
        return reverse('account', kwargs={'pk': self.object.pk})