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
  
  paginate_by = 100
    
  def get_queryset(self):
    qs = super().get_queryset()
    
    party = self.request.GET.get('party_affiliation')
    voter_score = self.request.GET.get('voter_score')
    
    min_dob = self.request.GET.get('min_dob')
    max_dob = self.request.GET.get('max_dob')
    
    v20state = self.request.GET.getlist('v20state')
    v21town = self.request.GET.getlist('v21town')
    v21primary = self.request.GET.getlist('v21primary')
    v22general = self.request.GET.getlist('v22general')
    v23town = self.request.GET.getlist('v23town')

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
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['years'] = range(1900, 2006)
    return context

class ShowVoterView(DetailView):
  '''Class for the /voter/<int:pk> page that shows a singular voter'''
  model = Voter
  template_name = 'voter_analytics/voter.html'
  context_object_name = 'voter'

class GraphView(ListView):
  model = Voter
  template_name = 'voter_analytics/graphs.html'
  context_object_name = 'voters'
  
  def get_queryset(self):
    qs = super().get_queryset()
    
    party = self.request.GET.get('party_affiliation')
    voter_score = self.request.GET.get('voter_score')
    
    min_dob = self.request.GET.get('min_dob')
    max_dob = self.request.GET.get('max_dob')
    
    v20state = self.request.GET.getlist('v20state')
    v21town = self.request.GET.getlist('v21town')
    v21primary = self.request.GET.getlist('v21primary')
    v22general = self.request.GET.getlist('v22general')
    v23town = self.request.GET.getlist('v23town')

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
    '''
    Provide context variables for use in template
    '''
    # start with superclass context
    context = super().get_context_data(**kwargs)
    qs = self.get_queryset()
    
    context['years'] = range(1900, 2006)
    
    # How I found out about count
    # https://stackoverflow.com/questions/11418522/django-how-to-annotate-queryset-with-count-of-filtered-foreignkey-field
    affiliation_counts = (
        qs.values('party_affiliation').annotate(count=Count('party_affiliation')).order_by()
    )
    
    
    x = [item['party_affiliation'] for item in affiliation_counts]
    y = [item['count'] for item in affiliation_counts]

    
    fig = go.Pie(labels=x, values=y)
    title_text = f"Voter Affiliation Distribution"
    
    graph_voter_affiliation_distribution = plotly.offline.plot(
        {"data": [fig], 
        "layout_title_text": title_text,
        },
      auto_open=False, output_type="div",
    )

    elections = {
    '2020 State Election': qs.filter(v20state=True).count(),
    '2021 Town Election': qs.filter(v21town=True).count(),
    '2021 Primary Election': qs.filter(v21primary=True).count(),
    '2022 General Election': qs.filter(v22general=True).count(),
    '2023 Town Election': qs.filter(v23town=True).count(),
    }
    
    x = list(elections.keys())
    y = list(elections.values())
    
    fig = go.Bar(x=x, y=y)
    title_text="Voter Participation by Election"
    
    graph_voter_participation = plotly.offline.plot(
        {"data": [fig], 
        "layout_title_text": title_text,
        }, auto_open=False, output_type="div",
                                         
    )
    
    dob_counts = (
      qs.values('dob__year').annotate(count=Count('dob__year')).order_by('dob__year')
    )
    
    x = [item['dob__year'] for item in dob_counts]
    y = [item['count'] for item in dob_counts]
    
    fig = go.Bar(x=x, y=y)
    title_text="Voter Distribution by Birth Year"
    
    graph_voter_birth_year_distribution = plotly.offline.plot(
    {"data": [fig], 
    "layout_title_text": title_text,
    }, auto_open=False, output_type="div",
    )
    
    context['graph_voter_affiliation_distribution'] = graph_voter_affiliation_distribution
    
    context['graph_voter_participation'] = graph_voter_participation
    
    context['graph_voter_birth_year_distribution'] = graph_voter_birth_year_distribution
    
    return context