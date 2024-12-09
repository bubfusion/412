from django.contrib import admin
from .models import Account, Friend, SmokeGif, Team, Friend_Requests


admin.site.register(Account)
admin.site.register(Friend)
admin.site.register(Team)
admin.site.register(SmokeGif)
admin.site.register(Friend_Requests)