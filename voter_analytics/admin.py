from django.contrib import admin
from .models import Voter
# Register your models here.

# So I can inspect the data in the admin panel
admin.site.register(Voter)