from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''Class for profile creation form'''
    class Meta:
      model = Profile
      fields = ['first_name', 'last_name', 'city', 'email', 'pfp_url' ]

class CreateStatusForm(forms.ModelForm):
   '''Class for status update creation form'''
   class Meta:
      model = StatusMessage
      fields = ['message']

class UpdateProfileForm(forms.ModelForm):
   '''Class for updating a profile'''
   class Meta:
      '''Meta data for what can be updated (everything except first and last name)'''
      model = Profile
      fields = ['city', 'email', 'pfp_url' ]

class UpdateStatusMessageForm(forms.ModelForm):
   '''Class for updating a status'''
   class Meta:
      '''Meta data for what can be updated (message)'''
      model = StatusMessage
      fields = ['message']