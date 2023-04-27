from django import forms
from django.forms import Select

from authors.models import Category


class PostForm(forms.Form):
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)

class ChooseCategoryForm(forms.ModelForm):
    name = forms.ChoiceField(choices=[(c.id, c.name) for c in Category.objects.all()])
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
          'name': Select(attrs={'class': 'select'}),
      }