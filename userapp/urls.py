from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [



path("userlistview/",views.userlistview,name='userlistview'),
path("",views.userindex,name='userindex'),
path("userdetailsview/<int:book_id>/",views.userdetailsview,name="userdetailsview"),


path("add_to_cart/<int:book_id>/",views.add_to_cart,name='add_to_cart'),
path("cart/",views.viewcart,name='viewcart'),
path("increase_quantity/<int:item_id>/",views.increase_quantity,name='increase_quantity'),
path("decrease_quantity/<int:item_id>/",views.decrease_quantity,name='decrease_quantity'),
path("remove_item/<int:item_id>/",views.remove_item,name='remove_item'),

path('create_checkout_session',views.create_checkout_session,name='create_checkout_session'),
path('success',views.success,name='success'),
path('cancel',views.cancel,name='cancel'),




]