from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Publisher, Genre, Author



class Search (forms.Form):
	searchChoices = (
		('title', 'Title'), 
		('publisher', 'Publisher'), 
		('author', 'Author'), 
		('genre', 'Genre')
		)
	search_by = forms.ChoiceField(label="Search By", choices= searchChoices, initial='Title', required=True)
	user_input = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Type to search'}))


class AddBook (forms.Form):
	rate = (
		('1.0', 1.0),('1.5',1.5),
		('2.0', 2.0),('2.5', 2.5),
		('3.0', 3.0),('3.5', 3.5),
		('4.0', 4.0),('4.5', 4.5),
		('5.0', 5.0)
	)
	#disabled=True,initial=new_book_id,
	book_id = forms.IntegerField(label="ID", widget=forms.NumberInput(attrs={'placeholder': 'Book ID', 'class': 'form-control'}))
	book_title = forms.CharField(label="Book Title", required=True, widget=forms.TextInput(attrs={'placeholder': 'Book Title', 'class': 'form-control', 'id':'adbk_book_title'}))
	author = forms.CharField(label="Author", required=True, widget=forms.TextInput(attrs={'placeholder': "Book's Author", 'class': 'form-control', 'id':'adbk_author'}))
	genre = forms.CharField(label="Genre", required=True, widget=forms.TextInput(attrs={'placeholder': 'Book Genre', 'class': 'form-control', 'id':'adbk_genre'}))
	publisher = forms.CharField(label="Publisher", required=True, widget=forms.TextInput(attrs={'placeholder': 'Book Publisher', 'class': 'form-control', 'id':'adbk_publisher'}))
	pages = forms.IntegerField(label="Pages", required=True,  widget=forms.NumberInput(attrs={'placeholder': 'Number of Pages', 'class': 'form-control', 'id':'adbk_pages'}))
	rating = forms.ChoiceField(label="Rating", required=True, choices=rate,  widget=forms.Select(attrs={'placeholder': 'Book Rating', 'class': 'form-control', 'id':'adbk_rating'}))
	published_date = forms.DateField(label="Published_date", required=True, widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control', 'id':'adbk_published_date'}))

	


class DeleteBook(forms.Form):
	book_id = forms.IntegerField(label="ID", required=True, widget=forms.NumberInput(attrs={'placeholder':'Book ID', 'class': 'form-control'}))


class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

