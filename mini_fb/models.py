from django.db import models


# This Profile model will need to include the following data attributes: 
# first name, last name, city, email address, and a profile image url.
class Profile(models.Model):
    '''Encapsulate the profile of some user'''
    # data attributes of a Profile:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False)
    pfp_url = models.URLField(blank=True)
    
    def get_status_messages(self):
        return StatusMessage.objects.filter(profile=self).order_by('-published')
    
    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} by {self.last_name}'
    
class StatusMessage(models.Model):
  profile =  models.ForeignKey("Profile", on_delete=models.CASCADE)
  message = models.TextField(blank=False)
  published = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.message} at {self.published}'