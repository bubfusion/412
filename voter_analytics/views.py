from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go
from django.db.models import Count
class ShowAllView(ListView):
  '''Class for the /voter_analytics page that shows all voters'''
  model = Voter
  template_name = 'voter_analytics/voters.html'
  context_object_name = 'voters'
  
  # number of entries per page
  paginate_by = 100
    
  # filters and returns data based on filters user
  def get_queryset(self):
    qs = super().get_queryset()
    
    # Get checks if filter was applied
    party = self.request.GET.get('party_affiliation')
    voter_score = self.request.GET.get('voter_score')
    
    min_dob = self.request.GET.get('min_dob')
    max_dob = self.request.GET.get('max_dob')
    
    v20state = self.request.GET.getlist('v20state')
    v21town = self.request.GET.getlist('v21town')
    v21primary = self.request.GET.getlist('v21primary')
    v22general = self.request.GET.getlist('v22general')
    v23town = self.request.GET.getlist('v23town')

    # if filter was applied, filter the query set to get data just based on filters
    if party:
        qs = qs.filter(party_affiliation=party)
    if voter_score:
        qs = qs.filter(voter_score=voter_score)
    if min_dob:
      qs = qs.filter(dob__gte=min_dob)
    if max_dob:
      qs = qs.filter(dob__lte=max_dob)
    if v20state:
      qs = qs.filter(v20state=True)
    if v21town:
      qs = qs.filter(v21town = True)
    if v21primary:
      qs = qs.filter(v21primary = True)
    if v22general:
      qs = qs.filter(v22general = True)
    if v23town:
      qs = qs.filter(v23town = True)
      
    # returns filtered data and is ordered by name
    return qs.order_by('first_name', 'last_name')
  
  # gets all the years
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['years'] = range(1915, 2006)
    return context

class ShowVoterView(DetailView):
  '''Class for the /voter/<int:pk> page that shows a singular voter'''
  model = Voter
  template_name = 'voter_analytics/voter.html'
  context_object_name = 'voter'

class GraphView(ListView):
  '''Class for /graph page which shows graphs based on the voters'''
  model = Voter
  template_name = 'voter_analytics/graphs.html'
  context_object_name = 'voters'
  
  def get_queryset(self):
    '''Returns a filtered query set based on user params'''
    qs = super().get_queryset()
    
    # Checks if there was get request for specific filter
    party = self.request.GET.get('party_affiliation')
    voter_score = self.request.GET.get('voter_score')
    
    min_dob = self.request.GET.get('min_dob')
    max_dob = self.request.GET.get('max_dob')
    
    v20state = self.request.GET.getlist('v20state')
    v21town = self.request.GET.getlist('v21town')
    v21primary = self.request.GET.getlist('v21primary')
    v22general = self.request.GET.getlist('v22general')
    v23town = self.request.GET.getlist('v23town')

    # Applies filter if there was a get for it
    if party:
        qs = qs.filter(party_affiliation=party)
    if voter_score:
        qs = qs.filter(voter_score=voter_score)
    if min_dob:
      qs = qs.filter(dob__gte=min_dob)
    if max_dob:
      qs = qs.filter(dob__lte=max_dob)
    if v20state:
      qs = qs.filter(v20state=True)
    if v21town:
      qs = qs.filter(v21town = True)
    if v21primary:
      qs = qs.filter(v21primary = True)
    if v22general:
      qs = qs.filter(v22general = True)
    if v23town:
      qs = qs.filter(v23town = True)
    
    return qs.order_by('first_name', 'last_name')
  
  def get_context_data(self, **kwargs) :
    '''Provides context variables for use in the html template'''
    # get super class content and filtered querey set
    context = super().get_context_data(**kwargs)
    qs = self.get_queryset()
    
    # range of years for dropdown
    context['years'] = range(1915, 2006)
    
    # How I found out about count. Super handy!
    # https://stackoverflow.com/questions/11418522/django-how-to-annotate-queryset-with-count-of-filtered-foreignkey-field
    affiliation_counts = (
        qs.values('party_affiliation').annotate(count=Count('party_affiliation')).order_by()
    )
    
    
    # Loops through all the parties for x and y values
    x = [item['party_affiliation'] for item in affiliation_counts]
    y = [item['count'] for item in affiliation_counts]

    
    # Creates a pie chart based on the data
    fig = go.Pie(labels=x, values=y)
    title_text = f"Voter Affiliation Distribution"
    
    # generates html for pie chart
    graph_voter_affiliation_distribution = plotly.offline.plot(
        {"data": [fig], 
        "layout_title_text": title_text,
        },
      auto_open=False, output_type="div",
    )

    # uses the qs to get the count of all trues for each election
    elections = {
    '2020 State Election': qs.filter(v20state=True).count(),
    '2021 Town Election': qs.filter(v21town=True).count(),
    '2021 Primary Election': qs.filter(v21primary=True).count(),
    '2022 General Election': qs.filter(v22general=True).count(),
    '2023 Town Election': qs.filter(v23town=True).count(),
    }
    
    # converts all key-value pairs to lists in order to act as x and y values
    x = list(elections.keys())
    y = list(elections.values())
    
    # creates bar chart
    fig = go.Bar(x=x, y=y)
    title_text="Voter Participation by Election"
    
    # gets the html for the chart
    graph_voter_participation = plotly.offline.plot(
        {"data": [fig], 
        "layout_title_text": title_text,
        }, auto_open=False, output_type="div",
                                         
    )
    
    # uses count again on the query set to get the count of each person born
    # in each year
    dob_counts = (
      qs.values('dob__year').annotate(count=Count('dob__year')).order_by('dob__year')
    )
    
    # loops through all years and counts for x and y values
    x = [item['dob__year'] for item in dob_counts]
    y = [item['count'] for item in dob_counts]
    
    # creates bar chart
    fig = go.Bar(x=x, y=y)
    title_text="Voter Distribution by Birth Year"
    
    # gets HTML for chart
    graph_voter_birth_year_distribution = plotly.offline.plot(
    {"data": [fig], 
    "layout_title_text": title_text,
    }, auto_open=False, output_type="div",
    )
    
    # Adds all newly created charts to context list
    context['graph_voter_affiliation_distribution'] = graph_voter_affiliation_distribution
    
    context['graph_voter_participation'] = graph_voter_participation
    
    context['graph_voter_birth_year_distribution'] = graph_voter_birth_year_distribution
    
    # returns all the context
    return context