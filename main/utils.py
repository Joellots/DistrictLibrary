import requests
import logging
from django.conf import settings
from .models import Book
from .filters import BookFilter
from datetime import datetime

logger = logging.getLogger(__name__)

def send_telegram_message(chat_id, message):
    token = settings.TELEGRAM_BOT_TOKEN
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    response = requests.post(url, data=data)
    logger.debug(response.text)  # Log the API response text
    return response.json()

def process_telegram_event(event):
    message = event.get('message', {})
    text = message.get('text', '').strip()
    chat_id = message.get('chat', {}).get('id')
    user_id = str(message.get('from', {}).get('id'))

    is_admin = user_id in settings.TELEGRAM_BOT_ADMINS

    if text.startswith('/latest'):
        response_message = get_latest_books()
        send_telegram_message(chat_id, response_message)

    elif text.startswith('/search'):
        query = text.split(' ', 1)[1] if len(text.split(' ', 1)) > 1 else ''
        response_message = search_books(query)
        send_telegram_message(chat_id, response_message)

    elif text.startswith('/publishers'):
        if is_admin:
            response_message = get_publisher_list()
            send_telegram_message(chat_id, response_message)
        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

    elif text.startswith('/genres'):
        if is_admin:
            response_message = get_genre_list()
            send_telegram_message(chat_id, response_message)
        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

    elif text.startswith('/authors'):
        if is_admin:
            response_message = get_author_list()
            send_telegram_message(chat_id, response_message)
        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

    if text.startswith('/addbook'):
        # Extracting the arguments from the command text
        if is_admin:
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_telegram_message(chat_id, "Please specify the book arguments inorder to add.")
                return

            arguments = parts[1]
            response_message = add_book(chat_id, arguments)
            
        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

        send_telegram_message(chat_id, response_message)


    if text.startswith('/deletebook'):
        # Extracting the book name from the command text
        if is_admin:
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_telegram_message(chat_id, "Please specify the book name to delete.")
                return

            book_name = parts[1]
            response_message = delete_book_by_name(chat_id, book_name)

        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

        send_telegram_message(chat_id, response_message)

    if text.startswith('/deletepublisher'):
        # Extracting the publisher name from the command text
        if is_admin:
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_telegram_message(chat_id, "Please specify the publisher name to delete.")
                return

            publisher_name = parts[1]
            response_message = delete_publisher(chat_id, publisher_name)

        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

        send_telegram_message(chat_id, response_message)

    if text.startswith('/deleteauthor'):
        # Extracting the author name from the command text
        if is_admin:
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_telegram_message(chat_id, "Please specify the author name to delete.")
                return

            author_name = parts[1]
            response_message = delete_author(chat_id, author_name)

        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

        send_telegram_message(chat_id, response_message)

    if text.startswith('/deletegenre'):
        # Extracting the genre name from the command text
        if is_admin:
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_telegram_message(chat_id, "Please specify the genre name to delete.")
                return

            genre_name = parts[1]
            response_message = delete_genre(chat_id, genre_name)

        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

        send_telegram_message(chat_id, response_message)

    if text.startswith('/help') or text.startswith('/start'):
        if is_admin:
            parts = text.split(maxsplit=1)
            if len(parts) < 2:
                send_telegram_message(chat_id, "Пожалуйста, укажите допустимый язык <Please specify the a valid language>: rus, eng")
                return
            lang = parts[1]
            display_help_message(chat_id, lang)
        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")

    if text.startswith('/finish'):
        if is_admin:

            display_finish_message(chat_id)
        else:
            send_telegram_message(chat_id, "Sorry, you're not authorized to use this command.")
def get_latest_books():
    # Fetch the latest 5 books from your database
    latest_books = Book.objects.all().order_by('-published_date')[:5]
    if not latest_books.exists():
        return "No latest books found."

    message_lines = ["Latest Books:"]      
    for book in latest_books:
        # Assuming you want to include the name and price in the message
        # Adjust the fields as per your Book model
        message_lines.append(f"{book.title} - Date Published: {book.published_date}")

    return "\n".join(message_lines)

def search_books(query):
    from .models import Genre, Publisher, Author
    # Assuming 'name' is a field on your Book model
    args = query.strip().split(',')
    print(args)
    matching_books = Book.objects
    for arg in args:
        if arg.split(":")[0] == 'T':
            title = arg.split(':')[1]
            matching_books = matching_books.filter(title__icontains=title)
        if arg.split(":")[0] == 'A':
            author = arg.split(':')[1]
            obj = Author.objects.get(Full_Name=author)
            matching_books = matching_books.filter(author__Full_Name=obj.Full_Name)
        if arg.split(":")[0] == 'G':
            genre = arg.split(':')[1]
            obj = Genre.objects.get(name=genre)
            matching_books = matching_books.filter(genre__name=obj.name)
        if arg.split(":")[0] == 'P':
            publisher = arg.split(':')[1]
            obj = Publisher.objects.get(name=publisher)
            matching_books = matching_books.filter(publisher__name=obj.name)
        if arg.split(":")[0] == 'p':
            pages =int(arg.split(':')[1])
            matching_books = matching_books.filter(pages__exact=pages)
        if arg.split(":")[0] == 'R':
            rating = str(arg.split(':')[1])
            matching_books = matching_books.filter(rating__exact=rating)
        if arg.split(":")[0] == 'D':
            published_date = datetime.strptime(arg.split(':')[1], '%m/%d/%Y').date()
            print(published_date)
            matching_books = matching_books.filter(published_date__exact=published_date)

    if not matching_books.exists():
        return "No books found matching your query."

    message_lines = ["Search Results:"]
    for i, book in enumerate(matching_books):
        # Customize this message format as needed
        message_lines.append(f"{i+1}) {book.title} - Author: {book.author.all()} - Genre: {book.genre.all()} - Publisher: \
            {book.publisher.all()}\n")

    return "\n".join(message_lines)

def get_publisher_list():
    from .models import Publisher  # Import the Publisher model
    publishers = Publisher.objects.all()
    if not publishers.exists():
        return "No publisher found."

    message_lines = ["Available Publishers:"]
    for publisher in publishers:
        # Assuming the Publisher model has a 'name' field
        message_lines.append(f"- {publisher.name}")

    return "\n".join(message_lines)

def get_author_list():
    from .models import Author  # Import the Author model
    authors = Author.objects.all()
    if not authors.exists():
        return "No author found."

    message_lines = ["Available Authors:"]
    for author in authors:
        # Assuming the Author model has a 'name' field
        message_lines.append(f"- {author.Full_Name}")

    return "\n".join(message_lines)

def get_genre_list():
    from .models import Genre  # Import the Genre model
    genres = Genre.objects.all()
    if not genres.exists():
        return "No Genre found."

    message_lines = ["Available Genres:"]
    for genre in genres:
        # Assuming the Genre model has a 'name' field
        message_lines.append(f"- {genre.name}")

    return "\n".join(message_lines)
def delete_book_by_name(chat_id, book_name):
    from .models import Book
    # Ensure that only admins can delete books
    if str(chat_id) not in settings.TELEGRAM_BOT_ADMINS:
        return "You do not have permission to delete books."

    # Fetch products with the given name (case insensitive)
    matching_books = Book.objects.filter(title__iexact=book_name)
    
    if not matching_books.exists():
        return "Book not found."

    matching_books.first().delete()

def delete_publisher(chat_id, publisher_name):
    from .models import Publisher
    # Ensure that only admins can delete books
    if str(chat_id) not in settings.TELEGRAM_BOT_ADMINS:
        return "You do not have permission to delete publishers."

    # Fetch products with the given name (case insensitive)
    matching_publishers = Publisher.objects.filter(name__iexact=publisher_name)
    
    if not matching_publishers.exists():
        return "Publisher not found."

    matching_publishers.first().delete()

def delete_author(chat_id, author_name):
    from .models import Author
    # Ensure that only admins can delete books
    if str(chat_id) not in settings.TELEGRAM_BOT_ADMINS:
        return "You do not have permission to delete authors."

    # Fetch products with the given name (case insensitive)
    matching_authors = Author.objects.filter(Full_Name__iexact=author_name)
    
    if not matching_authors.exists():
        return "Author not found."

    matching_authors.first().delete()

def delete_genre(chat_id, genre_name):
    from .models import Genre
    # Ensure that only admins can delete books
    if str(chat_id) not in settings.TELEGRAM_BOT_ADMINS:
        return "You do not have permission to delete genres."

    # Fetch products with the given name (case insensitive)
    matching_genres = Genre.objects.filter(name__iexact=genre_name)
    
    if not matching_genres.exists():
        return "Genre not found."

    matching_genres.first().delete()

def add_book(chat_id, arguments):
    from .models import Publisher, Genre, Author
    # Ensure that only admins can add books
    if str(chat_id) not in settings.TELEGRAM_BOT_ADMINS:
        send_telegram_message(chat_id, "You do not have permission to add books.")
        return "You do not have permission to add books."

    args = arguments.strip().split(',')
    print(args)
    book_id, title, author, genre, publisher, pages, rating, published_date = args
    bood_id = int(book_id)
    pages = int(pages)
    rating = str(rating)
    published_date = datetime.strptime(published_date, '%m/%d/%Y').date()

    bk = Book.objects
    pb = Publisher.objects
    gn = Genre.objects
    aut = Author.objects

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
        send_telegram_message(chat_id, "Choosen Book ID is UNAVAILABLE.")    
        return "Choosen Book ID is UNAVAILABLE."

def display_help_message(chat_id, lang):

    if "rus" in lang:
        help_message = """
    Добро пожаловать в бот районной библиотечной системы!

    Вот доступные команды:
    /start - Начало сеанса и отображение этого сообщения помощи.
    /finish - Завершение сеанса.

    /latest - Отобразить последние опубликованные книги.
    /search - Поиск книг по заданным параметрам.
    /publishers - Показать список издателей.
    /genres - Показать список жанров.
    /authors - Показать список авторов.

    /addbook - Добавить новую книгу в базу данных.
    /deletebook - Удалить книгу из базы данных.
    /deletepublisher - Удалить издателя из базы данных.
    /deleteauthor - Удалить автора из базы данных.
    /deletegenre - Удалить жанр из базы данных.
    """
    else:
        help_message = """
    Welcome to the District Library System Bot!

    Here are the available commands:
    - /latest: Get the latest 5 books.
    - /search <query>: Search for books based on title, author, genre, publisher, pages, rating, or published date.
    - /publishers: Get a list of available publishers.
    - /genres: Get a list of available genres.
    - /authors: Get a list of available authors.
    - /addbook <arguments>: Add a new book to the database. Arguments should be provided in the format:
        /addbook <book_id>,<title>,<author>,<genre>,<publisher>,<pages>,<rating>,<published_date>
    - /deletebook <book_name>: Delete a book by its name.
    - /deletepublisher <publisher_name>: Delete a publisher by its name.
    - /deleteauthor <author_name>: Delete an author by their name.
    - /deletegenre <genre_name>: Delete a genre by its name.
    """

    send_telegram_message(chat_id, help_message)

def display_finish_message(chat_id):
    finish_message = """Thank you for using the District Library System Bot!

You have finished your session. If you need further assistance, feel free to contact us.

Have a great day!
    """

    send_telegram_message(chat_id, finish_message)
