from django.contrib import admin


# Registers profile so they can be added from admin page
from .models import Profile, StatusMessage, Image, Friend

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)