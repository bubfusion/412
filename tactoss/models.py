from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
  '''Encapsulates a account on the website'''
  # Ties user to a account
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # What people want their display name to be
  display_name = models.TextField(blank=False)
  email = models.EmailField(blank=False)
  # Steam url for a user so other user's can quickly add each other
  steam_url = models.URLField(blank=True)
  # Discord username so players can add each other to talk
  discord_username = models.TextField(blank=True)
  account_picture = models.ImageField(blank=True)
  join_date = models.DateField(auto_now_add=True)
  
  def __str__(self):
    '''Returns string form of a account'''
    return f'{self.display_name}'

class Team(models.Model):
  '''Encapulates a team of users who will play together'''
  # Leader of the party. Every team must have a leader so it is not optional
  # If the leader disbands the team, the team deletes
  team_leader = models.ForeignKey(
      Account, 
      on_delete=models.CASCADE, 
      blank=False, 
      null=False
  )
  # Other people in the team. These can be optional as a team waits to fill
  # or if they want to run a team with less than 5 players
  account_2 = models.ForeignKey(
      Account, 
      on_delete=models.SET_NULL, 
      related_name="team_account_2",
      blank=True, 
      null=True
  )
  account_3 = models.ForeignKey(
      Account, 
      on_delete=models.SET_NULL, 
      related_name="team_account_3",
      blank=True, 
      null=True
  )
  account_4 = models.ForeignKey(
      Account, 
      on_delete=models.SET_NULL, 
      related_name="team_account_4",
      blank=True, 
      null=True
  )
  account_5 = models.ForeignKey(
      Account, 
      on_delete=models.SET_NULL, 
      related_name="team_account_5",
      blank=True, 
      null=True
  )
  
  # Sets if the team is open for new players to join/is visable on page
  is_open = models.BooleanField()
  
  def slot_open(self):
    if self.is_open == False:
      return False
    elif self.account_2 != None and self.account_3  != None and self.account_4 != None and self.account_5 != None:
      return False
    else:
      return True
  
  def in_team_already(self, account):
    if self.account_2 == account:
      return True
    elif self.account_3 == account:
      return True
    elif self.account_4 == account:
      return True
    elif self.account_5 == account:
      return True
    else:
      return False
    
  
  def add_player(self, account):
    if self.account_2 == None:
      self.account_2 = account
    elif self.account_3 == None:
      self.account_3 = account
    elif self.account_4 == None:
      self.account_4 = account
    elif self.account_5 == None:
      self.account_5 = account
    self.save()
      
  def __str__(self):
    '''Returns string form of a team'''
    return f'{self.team_leader}\'s team'
  


  
class SmokeGif(models.Model):
  '''Encapsulates a gif on how to use utility for a specific map by a specific
  user'''
  # User who posted the gif
  account = models.ForeignKey(Account, on_delete=models.CASCADE)
  # Gif of how to use the utility in game
  gif = models.ImageField()
  # The map which the gif is for
  map = models.TextField()
  # The area which the gif shows how to use utility for
  area = models.TextField()
  published = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    '''Returns string form of smokegif'''
    return f'{self.account}\'s smoke for {self.area} on {self.map}'
  
class Friend(models.Model):
   '''Encapsulates a friend relationship between 2 users'''
   profiel1 = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account1")
   account2 = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account2")

   def __str__(self):
    '''Returns string form of status'''
    return f'{self.profiel1} & {self.account2}'