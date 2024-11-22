from django.db import models

class User(models.Model):
  '''Encapsulates a user on the website'''
  # What people want their display name to be
  display_name = models.TextField(blank=False)
  email = models.EmailField(blank=False)
  # Steam url for a user so other user's can quickly add each other
  steam_url = models.URLField(blank=True)
  # Discord username so players can add each other to talk
  discord_username = models.TextField(blank=True)
  profile_picture = models.ImageField(blank=True)
  
  def __str__(self):
    '''Returns string form of a user'''
    return f'{self.display_name}'

class Team(models.Model):
  '''Encapulates a team of users who will play together'''
  # Leader of the party. Every team must have a leader so it is not optional
  # If the leader disbands the team, the team deletes
  team_leader = models.ForeignKey(
      User, 
      on_delete=models.CASCADE, 
      blank=False, 
      null=False
  )
  # Other people in the team. These can be optional as a team waits to fill
  # or if they want to run a team with less than 5 players
  user_2 = models.ForeignKey(
      User, 
      on_delete=models.SET_NULL, 
      related_name="team_user_2",
      blank=True, 
      null=True
  )
  user_3 = models.ForeignKey(
      User, 
      on_delete=models.SET_NULL, 
      related_name="team_user_3",
      blank=True, 
      null=True
  )
  user_4 = models.ForeignKey(
      User, 
      on_delete=models.SET_NULL, 
      related_name="team_user_4",
      blank=True, 
      null=True
  )
  user_5 = models.ForeignKey(
      User, 
      on_delete=models.SET_NULL, 
      related_name="team_user_5",
      blank=True, 
      null=True
  )
  
  def __str__(self):
    '''Returns string form of a team'''
    return f'{self.team_leader}\'s team'
  
  # Sets if the team is open for new players to join/is visable on page
  is_open = models.BooleanField()
  
class SmokeGif(models.Model):
  '''Encapsulates a gif on how to use utility for a specific map by a specific
  user'''
  # User who posted the gif
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # Gif of how to use the utility in game
  gif = models.ImageField()
  # The map which the gif is for
  map = models.TextField()
  # The area which the gif shows how to use utility for
  area = models.TextField()
  
  def __str__(self):
    '''Returns string form of smokegif'''
    return f'{self.user}\'s smoke for {self.area} on {self.map}'
  
class Friend(models.Model):
   '''Encapsulates a friend relationship between 2 users'''
   user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
   user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")

   def __str__(self):
    '''Returns string form of status'''
    return f'{self.user1} & {self.user2}'