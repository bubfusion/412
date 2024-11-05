from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# URL paths for mini_fb
urlpatterns = [
  path(r'', views.ShowAllView.as_view(), name = "show_all"), #url for showing all profiles
  path(r'mini_fb', views.ShowAllView.as_view(), name = "show_all"), #url for showing all profiles
  path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name = "profile"), # url for a specific profile
  path(r'create_profile', views.CreateProfileView.as_view(), name = "create_profile"), #URL for creating a profile
  path(r'status/create_status', views.CreateStatusMessageForm.as_view(), name = "create_status"), #URL for creating a status
  path(r'profile/update', views.UpdateProfileView.as_view(), name = "update_profile"), #URL for updating a profile
  path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name = "delete_status"), #URL for deleting a status message
  path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name = "update_status"), #URL for updating a status message
  path(r'profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name = "add_friend"), #URL for adding friend
  path(r'profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name = "friend_suggestions"), # url for friend suggestions
  path(r'profile/news_feed', views.ShowNewsFeedView.as_view(), name ="news_feed"), #news feed for a specific user
  path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name = "login"), #login page for a user
  path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name = "logout"), #logout page for a user
]