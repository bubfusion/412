from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
  '''Encapsulates a account on the website'''
  # Connects account to a user
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # What people want their display name to be
  display_name = models.TextField(blank=False)
  # Email address for account
  email = models.EmailField(blank=False)
  # Steam url for a user so other user's can quickly add each other (required)
  steam_url = models.URLField(blank=True)
  # Discord username so players can add each other to talk
  discord_username = models.TextField(blank=True)
  # Profile picture (has a default for people who don't upload one)
  account_picture = models.ImageField(blank=True, default='default.jpg')
  # Auto assigns date for when a user signed up
  join_date = models.DateField(auto_now_add=True)
  # Holds the team that a account is currently tied to 
  user_team = models.ForeignKey(
        'Team',
        on_delete=models.SET_NULL, #if a team is disbanned, sets this to null
        null=True, 
        blank=True,
    )
  # Many to many relationship for accounts to act as friends
  friends = models.ManyToManyField("Account", blank=True)
  # Accounts counter-strikes elo rating in the game
  elo_rating = models.IntegerField(blank=True, null=True)
  
  def get_outbound_requests(self):
    '''Gets friend requests sent by an account'''
    return Friend_Requests.objects.filter(from_account = self)
  
  def get_inbound_requests(self):
    '''Gets requests sent to an account'''
    return Friend_Requests.objects.filter(to_account = self)
  
  def __str__(self):
    '''Returns string form of a account'''
    return f'{self.display_name}'

class Friend_Requests(models.Model):
  '''Class that encapsulates a friend request'''
  # Account who sent friend request
  from_account = models.ForeignKey(Account, related_name= "from_account", on_delete=models.CASCADE)
  #Recipient of friend request
  to_account = models.ForeignKey(Account,related_name="to_account", on_delete=models.CASCADE)
  


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
    '''Returns if the team is joinable'''
    if self.is_open == False:
      return False
    elif self.account_2 and self.account_3 and self.account_4 and self.account_5:
      return False
    else:
      return True
  
  def in_team_already(self, account):
    '''Checks if an account is in current team'''
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
    '''Adds account to team'''
    if self.account_2 == None:
      self.account_2 = account
      account.user_team = self
      account.save()
    elif self.account_3 == None:
      self.account_3 = account
      account.user_team = self
      account.save()
    elif self.account_4 == None:
      self.account_4 = account
      account.user_team = self
      account.save()
    elif self.account_5 == None:
      self.account_5 = account
      account.user_team = self
      account.save()
    self.save()
    
  def get_average_elo(self):
    '''Gets the average elo rating of a team'''
    count = 0
    total_elo = 0
    for player in [self.team_leader, self.account_2, self.account_3, self.account_4, self.account_5]:
      # If there is a player in this spot and they have a rating, adds it to total
      # and updates count to a proper mean can be created
      if player != None and player.elo_rating != None:
        total_elo += player.elo_rating
        count+=1
    # Calculates and returns mean of average elo
    return int(total_elo/count)
  
  # This function I added later but is very helpful to simplify functions down
  def get_players(self):
    '''Returns all player slots of a team'''
    return [self.team_leader, self.account_2, self.account_3, self.account_4, self.account_5]
  
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
  