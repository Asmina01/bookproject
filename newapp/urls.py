from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

path("createbook/",views.creatbook, name='creatbook'),
    path("author/",views.creatauthor,name="author"),
    path("booklist/",views.listview,name='booklist'),
    path("detailsview/<int:book_id>/",views.detailsview,name='details'),
    path("updatebook/<int:book_id>/",views.updatebook,name='update'),
    path("deleteview/<int:book_id>/",views.deleteview,name='delete'),

    path('admin_index/',views.admin_index,name='admin_index'),
    path('userindex/',views.userindex,name='userindex'),

    path("search/",views.search_book,name='search'),
    path("registration/",views.registration,name="registration"),
    path("",views.loginuser,name="login"),

    path("logout/",views.logout,name="logout"),

    path("authorlist/",views.listauthor,name='authorlist'),
    path("deleteauthor/<int:author_id>/",views.deleteauthor,name='deleteauthor'),







]