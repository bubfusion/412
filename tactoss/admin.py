from django.contrib import admin
from .models import Account, SmokeGif, Team, Friend_Requests

# Registers models to be editable via admin
admin.site.register(Account)
admin.site.register(Team)
admin.site.register(SmokeGif)
admin.site.register(Friend_Requests)