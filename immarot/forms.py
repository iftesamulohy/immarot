from django import forms

from books.models import Author
from cms.models import Button


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'biography']
