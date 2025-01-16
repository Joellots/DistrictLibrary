from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import Book, Publisher, Genre, Author
from .forms import Search, AddBook, DeleteBook, SignUpForm
from .myglobals import userInput, srchBy
from .filters import BookFilter
from django.utils import timezone
from datetime import datetime
from hitcount.views import HitCountDetailView
from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_exempt
import logging
from .utils import process_telegram_event
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__name__)

# Create your views here.


def home(response):
	return render(response, "main/home.html", {})



def login_user(request):
	# password = None
	# user = authenticate(request, username=username, password=password)
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = username
		#Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "Login successful")
			#return redirect('/login/?username={}'.format(username))
			return render(request, "main/login.html", {"username":username})
		else:
			messages.success(request, "Error logging in. Please try again...")
			return redirect('login')

	else: 
		return render(request, "main/login.html")

@login_required(login_url='login')
def logout_user(request):
	logout(request)
	messages.success(request, "You have been logged out...")
	return redirect('login')

@login_required(login_url='login')
def search(request):
	#model objects
	bk = Book.objects
	pb = Publisher.objects
	gn = Genre.objects
	aut = Author.objects
	
	#making queryset for djangoFilter fields
	

	#CHECK IF LOGGED IN USER IS THE ADMIN BY ASIGNING USERNAME OF USER TO A VARIABLE
	username = None
	if request.user.is_authenticated:
		# username = request.user.username
		books = bk.all()
		book_count = books.count()

		#Calling djangoFilter and passing in values: request.GET and respective querysets
		bookFilter = BookFilter(request.GET, queryset=books)
		
		
		#Assigning filtered data to values_list
		#title_values = bookFilter.filters['title'].queryset
		#pages_values = bookFilter.filters['pages'].queryset
		books = bookFilter.qs
		#book_id = int(len(bk.values_list("id", flat=True)) + 1)

		context = {	
					"bk":bk,
					"bookFilter":bookFilter, 
					"books":books, 
					"book_count":book_count,
					}
		return render(request, "main/search.html", context)



@login_required(login_url='login')
def search_admin(request):
	#model objects
	bk = Book.objects
	pb = Publisher.objects
	gn = Genre.objects
	aut = Author.objects
	
	#making queryset for djangoFilter fields
	

	#CHECK IF LOGGED IN USER IS THE ADMIN BY ASIGNING USERNAME OF USER TO A VARIABLE
	username = None
	if request.user.is_authenticated:
		# username = request.user.username
		books = bk.all()
		book_count = books.count()

		#Calling djangoFilter and passing in values: request.GET and respective querysets
		bookFilter = BookFilter(request.GET, queryset=books)
		
		
		#Assigning filtered data to values_list
		#title_values = bookFilter.filters['title'].queryset
		#pages_values = bookFilter.filters['pages'].queryset
		books = bookFilter.qs
		
		#book_id = int(len(bk.values_list("id", flat=True)) + 1)

		if request.user.is_staff:

			if request.method == 'POST' and 'add_book_btn' in request.POST:

				# *diff for item in bk.values_list('id', flat=True):

				# if book_id in bk.values_list('id', flat=True):
				# 	messages.success(request, "Please input a different ID")
				# 	return redirect('search')/
				# else:
				
				formAddBook = AddBook(request.POST)

				if formAddBook.is_valid():
					book_id = formAddBook.cleaned_data['book_id']
					title = formAddBook.cleaned_data['book_title']
					author = formAddBook.cleaned_data['author']
					genre = formAddBook.cleaned_data['genre']
					publisher = formAddBook.cleaned_data['publisher']
					pages = formAddBook.cleaned_data['pages'] 
					rating = formAddBook.cleaned_data['rating']
					published_date = formAddBook.cleaned_data['published_date']

					if book_id not in bk.values_list('id', flat=True):
						new_book = Book(id=book_id, title = title, published_date=published_date, complete=False, rating=rating, pages=pages)
						new_book.save()
						if publisher not in  pb.values_list('name', flat=True):
							pb_new = Publisher(name=publisher)
							pb_new.save()
						if author not in aut.values_list('Full_Name', flat=True):
							aut_new = Author(Full_Name=author)
							aut_new.save()
						if genre not in gn.values_list('name', flat=True):
							gn_new = Genre(name=genre)
							gn_new.save()

						pb_add = pb.get(name=publisher)
						aut_add = aut.get(Full_Name=author)
						gn_add = gn.get(name=genre)

						bk.get(id=book_id).publisher.set([pb_add])
						bk.get(id=book_id).genre.set([gn_add])
						bk.get(id=book_id).author.set([aut_add])
					else:
						context = {	
							"bk":bk,
							"book_id":book_id,
							"bookFilter":bookFilter, 
							#"formAddBook":formAddBook,
							"username":username
						}
						messages.success(request, "Choosen Book ID is UNAVAILABLE")
						return redirect('main/search_admin.html', context)


			if request.method == "POST" and 'delete_book_btn' in request.POST:

				formDeleteBook = DeleteBook(request.POST)

				if formDeleteBook.is_valid():
					book_id_del = formDeleteBook.cleaned_data['book_id']
	
					if book_id_del not in bk.values_list("id", flat=True):
						messages.success(request, 'Please Input a Valid Book ID') 
						return redirect('main/search_admin.html')
					else:
						del_book = bk.filter(id=book_id_del)
						del_book.delete()		


			formAddBook = AddBook()
			formDeleteBook = DeleteBook()

			context = {	
						"bk":bk,
						"bookFilter":bookFilter, 
						"books":books, 
						"book_count":book_count,
						"formAddBook":formAddBook,
						"formDeleteBook":formDeleteBook,
					}
			return render(request, "main/search_admin.html", context)
		else:
			context = {	
						"bk":bk,
						"bookFilter":bookFilter, 
						"books":books, 
						"book_count":book_count,
						}
			return render(request, "main/search_admin/html", context)

		#return HttpResponse(response, "main/search_result.html", {'myArray':myArray})

def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			#Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered!")

			return redirect('/login/?username={}'.format(username))
	
	else:
		form = SignUpForm()
		return render(request, 'main/register.html', {'form':form})


	return render(request, 'main/register.html', {'form':form})


def update_last_activity(request):
	if request.user.is_authenticated:
		request.session['last_activity'] = str(datetime.strptime(str(timezone.now()),"%Y-%m-%d %H:%M:%S.%f%z"))
		return JsonResponse({'status': 'success'})
	else:
		return JsonResponse({'status': 'error'})

	
def search_result(request):
	return render(request, 'main/search_result.html')



def jsonData(request):
	bk = Book.objects

	userInput = ''

	if userInput != '':

		formSearch = Search(request.POST)
		title_list = []
		author_list = []
		genre_list = []
		publisher_list = []	
		pages_list = []
		rating_list = []
		published_date_list = []
		key_list = []
				
		for item in bk.values_list("id", flat=True):

			#if srchBy == 'title':
			if userInput == str(bk.get(id=item).title):
				
				key_list.append(item)
				title_list.append(bk.get(id=item).title)
				pages_list.append(bk.get(id=item).pages)
				rating_list.append(bk.get(id=item).rating)
				published_date_list.append(bk.get(id=item).published_date)

				
				for author in bk.get(id=item).author_set.values_list('Full_Name', flat=True):
					author_list.append(author)

				for genre in bk.get(id=item).genre_set.values_list('name', flat=True):
					genre_list.append(genre)

				for publisher in bk.get(id=item).publisher_set.values_list('name', flat=True):
					publisher_list.append(publisher)

		context = {
					'json_key': key_list,
					'json_title':title_list,
					'json_author':author_list,
					'json_genre':genre_list,
					'json_publisher':publisher_list,
					'json_pages':pages_list,
					'json_rating':rating_list,
					'json_published_date':published_date_list,
					'srchBy':srchBy,
					'userInput':userInput,
				}

		myArray = []
		myDict = {}
		for item in range(len(context["json_key"])):
			myDict.update({"id": (context["json_key"])[item]})
			myDict.update({"title": (context["json_title"])[item]})
			myDict.update({"author": (context["json_author"])[item]})
			myDict.update({"genre": (context["json_genre"])[item]})
			myDict.update({"publisher": (context["json_publisher"])[item]})
			myDict.update({"pages": (context["json_pages"])[item]})
			myDict.update({"rating": (context["json_rating"])[item]})
			myDict.update({"published_date": (context["json_published_date"])[item]})
			myArray.append(myDict)
			if item != len(context['json_key'])-1:
				myDict.clear()

		
		return JsonResponse({"myArray":myArray})


		#return render(request, 'main/search_result.html', context)


	elif userInput == None:
		formSearch = Search()

	return HttpResponse("<h2><i style = 'display: block; text-align: center; color: red;'>Invalid</i></h2>")

	#return render(request, "main/search.html", {"formSearch":formSearch, "bk":bk})
		#return JsonResponse()

@csrf_exempt
@require_http_methods(['POST'])
def telegram_webhook(request):
    try:
        update = json.loads(request.body.decode('utf-8'))
        process_telegram_event(update)
        return JsonResponse({'ok': True})
    except Exception as e:
        logger.error(f"Error processing telegram event: {e}")
        return JsonResponse({'ok': False}, status=400)

	


