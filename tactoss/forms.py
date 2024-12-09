from django import forms
from .models import Account

class CreateAccountForm(forms.ModelForm):
    '''Class for profile creation form'''
    class Meta:
      model = Account
      fields = ['display_name', 'email', 'steam_url', 'discord_username', 'elo_rating']