from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Book(models.Model):
	rate = (
		('1.0', 1.0),('1.5',1.5),
		('2.0', 2.0),('2.5', 2.5),
		('3.0', 3.0),('3.5', 3.5),
		('4.0', 4.0),('4.5', 4.5),
		('5.0', 5.0)
	)
	title = models.CharField(max_length=200)
	pages = models.IntegerField()
	rating = models.CharField(max_length=10, choices=rate)
	published_date = models.DateField()
	complete = models.BooleanField()
	publisher = models.ManyToManyField("Publisher")
	genre = models.ManyToManyField("Genre")
	author = models.ManyToManyField("Author")

	def __str__(self):
		return f'{self.title} - {self.published_date.strftime("%Y-%m-%d")}'

class Publisher(models.Model): 
	name = models.CharField(max_length=200)

	def __str__ (self):
		return self.name


class Genre(models.Model):
	name = models.CharField(max_length=100)

	def __str__ (self):
		return self.name


class Author(models.Model):
	Full_Name = models.CharField(max_length=100)

	def __str__ (self):
		return self.Full_Name

	