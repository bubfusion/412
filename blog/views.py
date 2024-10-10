import random
from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import *


# classed based view

class ShowAllView(ListView):
  model = Article
  template_name = 'blog/show_all.html'
  context_object_name = 'articles'


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

