from django.db import models
from django.contrib.auth.models import User


# This Profile model will need to include the following data attributes: 
# first name, last name, city, email address, and a profile image url.
class Profile(models.Model):
    '''Encapsulate the profile of some user'''
    # data attributes of a Profile:
    user = models.ForeignKey(User, on_delete=models.CASCADE) #fk to a user account
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    pfp_url = models.URLField(blank=True)
    
    def get_status_messages(self):
        '''Returns statuses for users'''
        return StatusMessage.objects.filter(profile=self).order_by('-published')
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_friends(self):
      '''Returns all friends for this profile.'''

      #https://docs.djangoproject.com/en/5.1/ref/models/querysets/ 
      #for how I learned query sets
      friends_as_profile1 = Friend.objects.filter(profile1=self).values_list('profile2', flat=True)
      friends_as_profile2 = Friend.objects.filter(profile2=self).values_list('profile1', flat=True)
    
      friend_ids = set(friends_as_profile1).union(friends_as_profile2)
      return Profile.objects.filter(id__in=friend_ids)
    
    def add_friend(self, other):
       '''Adds self and other profile as friends if not already'''
       if self == other:
          print("You can't friend yourself!")
          return
       
       are_friends = (Friend.objects.filter(profile1=self, profile2=other).exists() or 
                      Friend.objects.filter(profile1=other, profile2=self).exists())
       
       if not are_friends:
          Friend.objects.create(profile1=self, profile2=other)
       else:
          print("You are already friends with that user!")
       return
       
    def get_friend_suggestions(self):
      '''Gets suggested friends for a user '''
      
      # Very simple way of doing this. It just gets all of the users minus current
      # profile and current friends and returns them
      all_users_exlcuding_self = Profile.objects.exclude(pk=self.pk)
      friends = self.get_friends()
      suggestions = all_users_exlcuding_self.exclude(pk__in=friends.values_list('pk', flat=True))
      return suggestions
    
    def get_news_feed(self):
      '''Returns the news feed for a profile'''
      
      #Gets friends and statuses for current user
      all_status = StatusMessage.objects.filter(profile=self)
      friends = self.get_friends()
      
      # Appends statuses of all friends to the list
      for friend in friends:
        all_status = all_status | StatusMessage.objects.filter(profile=friend)
        
      all_status = all_status.order_by('-published').distinct()
      return all_status
      
      
      
    
class StatusMessage(models.Model):
  '''Encapsulate the status message of some profile'''
  profile =  models.ForeignKey("Profile", on_delete=models.CASCADE) #if profile deleted, statuses go with it
  message = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)

  def __str__(self):
    '''Returns string form of status'''
    return f'{self.message} at {self.published}'
  
  def get_images(self):
    '''Returns all images for the status'''
    return Image.objects.filter(statusMessage=self)

  
class Image(models.Model):
  '''Encapsulate the image of some status'''
  # foreign key is the status it is attached to
  # zero to many
  statusMessage = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)
  # Uploaded Image
  image = models.ImageField(blank=True)
  # Time the image was published
  published = models.DateTimeField(auto_now=True)

class Friend(models.Model):
   '''Encapsulates a friend relationship between 2 profiles'''
   profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
   profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")

   def __str__(self):
    '''Returns string form of status'''
    return f'{self.profile1} & {self.profile2}'