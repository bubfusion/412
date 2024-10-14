from django.urls import path
from django.conf import settings
from . import views

# URL paths for mini_fb
urlpatterns = [
  path(r'', views.ShowAllView.as_view(), name = "show_all"), #url for showing all profiles
  path(r'mini_fb', views.ShowAllView.as_view(), name = "show_all"), #url for showing all profiles
  path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name = "profile"), # url for a specific profile
  path(r'create_profile', views.CreateProfileView.as_view(), name = "create_profile"), #URL for creating a profile
  path(r'profile/<int:pk>/create_status', views.CreateStatusMessageForm.as_view(), name = "create_status"), #URL for creating a status
  
]