from django.urls import path, include
from . import views
from .views import update_last_activity
from .views import telegram_webhook

urlpatterns = [
path("", views.home, name="home"),
path("search/", views.search, name="search"),
path("jsonData/", views.jsonData, name="jsonData"),
path("login/", views.login_user, name='login'),
path("logout/", views.logout_user, name='logout'),
path("register/", views.register_user, name='register'),
path("search_admin/", views.search_admin, name="search_admin"),
path("update-last-activity/", update_last_activity, name="update_last_activity"),
path('telegram/webhook/', views.telegram_webhook, name='telegram_webhook'),
#path("search/", views.book_add, name="book_add"),
#path("search/", views.book_delete, name="book_delete"),
#path("search_result/", views.search_result, name="search_result"),

]