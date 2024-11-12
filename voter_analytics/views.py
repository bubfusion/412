from django.shortcuts import render
from django.views.generic import ListView
from .models import Voter

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
