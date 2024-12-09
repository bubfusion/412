from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# URL paths for restaurant
urlpatterns = [
  path(r'', views.ShowHome.as_view(), name = "home"),
  path(r'account/<int:pk>', views.ShowAccountPageView.as_view(), name = "account"), # url for a specific account
  path(r'teams', views.ShowTeamsView.as_view(), name = "teams"), # url for a specific account
  path(r'teams/join/<int:pk>', views.JoinTeamView.as_view(), name = "join_team"),
  path(r'teams/<int:pk>', views.ShowTeamPageView.as_view(), name = "team"),
  path(r'teams/create', views.CreateTeam.as_view(), name = "create_team"),
  path(r'teams/leave', views.LeaveTeam.as_view(), name = "leave"),
  path(r'send_friend_request/<int:request_pk>', views.SendFriendRequest.as_view(), name = "send_friend_request"),
  path(r'accept_friend_request/<int:request_pk>', views.AcceptFriendRequest.as_view(), name="accept_friend_request"),
  path(r'friends', views.FriendStatus.as_view(), name='friends'),
  path(r'cancel_friend_request/<int:request_pk>', views.CancelFriendRequest.as_view(), name="cancel_friend_request"),
  path(r'decline_friend_request/<int:request_pk>', views.DeclineFriendRequest.as_view(), name="decline_friend_request"),
  path('login/', auth_views.LoginView.as_view(template_name='tactoss/login.html'), name = "login"),
  path('logout/', auth_views.LogoutView.as_view(template_name='tactoss/home.html'), name = "logout"),
  path(r'create_account', views.CreateAccountView.as_view(), name = "create_account"), #URL for creating an account
  path(r'feed/', views.ShowFeedView.as_view(template_name='tactoss/feed.html'), name = "feed"),
  path(r'create_lineup', views.CreateLineuptView.as_view(), name = "create_lineup"),
]