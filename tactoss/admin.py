from django.contrib import admin
from .models import Account, Friend, SmokeGif, Team


admin.site.register(Account)
admin.site.register(Friend)
admin.site.register(Team)
admin.site.register(SmokeGif)