from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    class Meta:
      model = Profile
      fields = ['first_name', 'last_name', 'city', 'email', 'pfp_url' ]

class CreateStatusForm(forms.ModelForm):
   class Meta:
      model = StatusMessage
      fields = ['message',]