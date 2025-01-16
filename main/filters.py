import django_filters
from .models import *
from django import forms
from django_select2.forms import ModelSelect2MultipleWidget
from django.forms.widgets import Select

class BookFilter(django_filters.FilterSet):

	title = django_filters.CharFilter(lookup_expr='icontains', label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book title'}))
	#pages = django_filters.NumberFilter(lookup_expr='iexact', label=False, widget=forms.NumberInput(attrs={'min':0, 'max':5000, 'placeholder': 'pages'}))
	rating = django_filters.NumberFilter(lookup_expr='iexact', label=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':5, 'placeholder': 'Rating'}))
	publisher = django_filters.CharFilter(method='pub_filter', label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publisher'}))
	genre = django_filters.CharFilter(method='genre_filter', label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book genre'}))
	author = django_filters.CharFilter(method='author_filter', label=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author'}))
	

	class Meta:
		model = Book
		fields = '__all__'
		exclude = ['pages', 'published_date', 'complete']

	def pub_filter(self, queryset, name, value):
   		return queryset.filter(publisher__name__icontains=value)

	def genre_filter(self, queryset, name, value):
   		return queryset.filter(genre__name__icontains=value)

	def author_filter(self, queryset, name, value):
   		return queryset.filter(author__Full_Name__icontains=value)

