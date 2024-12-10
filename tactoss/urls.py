from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# URL paths for restaurant
urlpatterns = [
  path(r'', views.ShowHome.as_view(), name = "home"),
  path(r'account/<int:pk>', views.ShowAccountPageView.as_view(), name = "account"), # url for a specific account
  path(r'teams', views.ShowTeamsView.as_view(), name = "teams"), # shows all open teams
  path(r'teams/join/<int:pk>', views.JoinTeamView.as_view(), name = "join_team"), # join a team link
  path(r'teams/<int:pk>', views.ShowTeamPageView.as_view(), name = "team"), # view specific team
  path(r'teams/create', views.CreateTeam.as_view(), name = "create_team"), # create a team
  path(r'teams/leave', views.LeaveTeam.as_view(), name = "leave"), # leave a team
  path(r'send_friend_request/<int:request_pk>', views.SendFriendRequest.as_view(), name = "send_friend_request"), #send request to a user
  path(r'accept_friend_request/<int:request_pk>', views.AcceptFriendRequest.as_view(), name="accept_friend_request"), #accept a specific request
  path(r'friends', views.FriendStatus.as_view(), name='friends'), #view inbound and outbound requests and view current friends
  path(r'cancel_friend_request/<int:request_pk>', views.CancelFriendRequest.as_view(), name="cancel_friend_request"), # cancel an outgoing friend request
  path(r'decline_friend_request/<int:request_pk>', views.DeclineFriendRequest.as_view(), name="decline_friend_request"), # decline an inbound friend request
  path('login/', auth_views.LoginView.as_view(template_name='tactoss/login.html'), name = "login"), # Login to a user account
  path('logout/', auth_views.LogoutView.as_view(template_name='tactoss/home.html'), name = "logout"), # Logout of current account
  path(r'create_account', views.CreateAccountView.as_view(), name = "create_account"), #URL for creating an account
  path(r'feed/', views.ShowFeedView.as_view(template_name='tactoss/feed.html'), name = "feed"), #shows all smoke lineups
  path(r'create_lineup', views.CreateLineuptView.as_view(), name = "create_lineup"), # create a lineup to show on feed
  path(r'update_account', views.UpdateAccounteView.as_view(), name = "update_account"), # updates current logged in account
  
]