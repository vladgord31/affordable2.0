from typing import Literal
from django import forms

from main.models import Comments, Reviews

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields: tuple[Literal['text']] = ('text',)

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('title', 'text', 'rating',)
