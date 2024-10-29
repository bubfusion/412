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
  path(r'profile/<int:pk>/update', views.UpdateProfileView.as_view(), name = "update_profile"), #URL for updating a profile
  path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name = "delete_status"), #URL for deleting a status message
  path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name = "update_status"), #URL for updating a status message
  path(r'profile/<int:pk>/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name = "add_friend"), #URL for adding friend
  path(r'profile/<int:pk>/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name = "friend_suggestions"), # url for friend suggestions
  path(r'profile/<int:pk>/news_feed', views.ShowNewsFeedView.as_view(), name ="news_feed"), #news feed for a specific user
]