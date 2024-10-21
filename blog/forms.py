## write the CreateCommentForm
# blog/forms.py
from django import forms
from .models import Comment, Article
class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Comment
        fields = ['author', 'text', ]  # which fields from model should we use



class CreateArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['author', 'title', 'text', 'image_file']