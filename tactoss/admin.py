from django.contrib import admin
from .models import User, Friend, SmokeGif, Team


admin.site.register(User)
admin.site.register(Friend)
admin.site.register(Team)
admin.site.register(SmokeGif)