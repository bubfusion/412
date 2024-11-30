from django.urls import path
from django.conf import settings
from . import views

# URL paths for restaurant
urlpatterns = [
  path(r'', views.ShowHome.as_view(), name = "home"),
  path(r'account/<int:pk>', views.ShowAccountPageView.as_view(), name = "account"), # url for a specific account
  path(r'teams', views.ShowTeamsView.as_view(), name = "teams"), # url for a specific account
  path(r'teams/join/<int:pk>', views.ShowTeamsView.as_view(), name = "join_team"),
  path(r'teams/<int:pk>', views.ShowTeamPageView.as_view(), name = "team")
]