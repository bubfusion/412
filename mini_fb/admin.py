from django.contrib import admin


# Registers profile so they can be added from admin page
from .models import Profile
admin.site.register(Profile)