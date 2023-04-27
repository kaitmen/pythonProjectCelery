import django_filters
from django.forms import DateInput

from .models import Post


class PostFilter(django_filters.FilterSet):
   created_at__gt = django_filters.NumberFilter(field_name='created_at', lookup_expr='year__gt',
                                                 widget=DateInput(attrs={'type': 'date', 'placeholder': 'Date start'}))
   class Meta:
       model = Post
       fields = {

           'title': ['icontains'],
           'text': ['icontains'],
           'author__user__username': ['icontains'],

           'rating': [
               'lt',
               'gt',
           ],
       }