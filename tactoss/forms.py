from django import forms
from .models import Account, SmokeGif

class CreateAccountForm(forms.ModelForm):
    '''Class for profile creation form'''
    class Meta:
      model = Account
      fields = ['display_name', 'email', 'steam_url', 'discord_username', 'elo_rating']
      
class CreateLineupForm(forms.ModelForm):
  '''Class for lineup gif creation'''
  class Meta:
    model = SmokeGif
    fields = ['map', 'area']
    
class UpdateAccountForm(forms.ModelForm):
   '''Class for updating a profile'''
   class Meta:
      '''Meta data for what can be updated (everything except first and last name)'''
      model = Account
      fields = ['display_name', 'steam_url', 'discord_username', 'elo_rating']
