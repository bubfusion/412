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
      fields = ['message',]

class UpdateProfileForm(forms.ModelForm):
   class Meta:
      model = Profile
      fields = ['city', 'email', 'pfp_url' ]