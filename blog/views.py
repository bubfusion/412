import random
from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView
from django import forms
from .models import *
from .forms import *
from .forms import CreateCommentForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin


# classed based view

class ShowAllView(ListView):
  model = Article
  template_name = 'blog/show_all.html'
  context_object_name = 'articles'
  
  def dispatch(self, *args, **kwargs):
    print(f"ShowAllView.dispatch; request.user={self.request.user}")
    return super().dispatch(*args, **kwargs)


class RandomArticleView(DetailView):
  model = Article
  template_name = "blog/article.html"
  context_object_name = 'article'



  def get_object(self):
    all_articles = Article.objects.all()
    article = random.choice(all_articles)
    return article
  

class ArticleView(DetailView):
  model = Article
  template_name = "blog/article.html"
  context_object_name = 'article'


## write the CreateCommentView
# comments/views.py

class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        article = Article.objects.get(pk=self.kwargs['pk'])
        # print(article)
        form.instance.article = article
        return super().form_valid(form)
        
## also:  revise the get_success_url
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        return reverse('article', kwargs={'pk': self.kwargs['pk']})
    

class CreateArticleView(LoginRequiredMixin, CreateView):
   form_class = CreateArticleForm
   template_name = 'blog/create_article_form.html'

   def get_login_url(self) -> str:
      return reverse('login')
   def form_valid(self,form):
      user = self.request.user
      form.instance.user = user
      print(f'CreateArticleView(): form.cleaned_data={form.cleaned_data}')
      return super().form_valid(form)