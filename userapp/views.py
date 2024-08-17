from django.conf import settings
from django.contrib import auth,messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage
from django.urls import reverse

from newapp.models import Book
from .models import cartitem
from .models import Cart
import stripe



# Create your views here.






def userlistview(request):

    books=Book.objects.all()



    return render(request,'user/userlistview.html',{'books':books})


def userdetailsview(request,book_id):

    book=Book.objects.get(id=book_id)

    return render(request,'user/userdetailsview.html',{'book':book})


def userindex(request):
    # Logic for the user page
    return render(request, 'user/userindex.html')


def add_to_cart(request, book_id):
    if request.user.is_authenticated:
        try:
            book = Book.objects.get(id=book_id)
            if book.quantity > 0:
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart_item, item_created = cart.cartitem_set.get_or_create(book=book)

                if not item_created:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    cart_item.quantity = 1
                    cart_item.save()

                messages.success(request, 'Book added to cart successfully.')
            else:
                messages.error(request, 'Book is out of stock.')
        except Book.DoesNotExist:
            messages.error(request, 'Book not found.')
    else:
        messages.error(request, 'Please login to add items to the cart.')

    return redirect('viewcart')


def viewcart(request):
    if request.user.is_authenticated:
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.cartitem_set.all()
            total_price = sum(item.book.price * item.quantity for item in cart_items)
            total_items = cart_items.count()

            context = {
                'cart_items': cart_items,
                'total_price': total_price,
                'total_items': total_items
            }

            return render(request, 'user/cart.html', context)
        except Cart.DoesNotExist:
            messages.error(request, 'Error retrieving the cart.')

    else:
        messages.error(request, 'Please login first.')
        return redirect('login')

    # Default context in case of an exception or user not authenticated
    context = {
        'cart_items': [],
        'total_price': 0,
        'total_items': 0
    }

    return render(request, 'user/cart.html', context)


def increase_quantity(request, item_id):
    if request.user.is_authenticated:
        try:
            cart_item = cartitem.objects.get(id=item_id)
            if cart_item.quantity < cart_item.book.quantity:
                cart_item.quantity += 1
                cart_item.save()
        except cartitem.DoesNotExist:
            messages.error(request, 'Item not found.')

    return redirect('viewcart')

def decrease_quantity(request, item_id):
    if request.user.is_authenticated:
        try:
            cart_item = cartitem.objects.get(id=item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        except cartitem.DoesNotExist:
            messages.error(request, 'Item not found.')

    return redirect('viewcart')

def remove_item(request, item_id):
    if request.user.is_authenticated:
        try:
            cart_item = cartitem.objects.get(id=item_id)
            cart_item.delete()
        except cartitem.DoesNotExist:
            messages.error(request, 'Item not found.')

    return redirect('viewcart')


def create_checkout_session(request):
    cart_items=cartitem.objects.all()

    if cart_items:
        stripe.api_key=settings.STRIPE_SECRET_KEY

        if request.method=='POST':

            line_items=[]
            for cart_item in cart_items:
                if cart_item.book:
                    line_item={
                        'price_data':{
                            'currency':'INR',
                            'unit_amount':int(cart_item.book.price * 100),
                            'product_data':{
                                'name':cart_item.book.title
                            },
                        },
                        'quantity':1

                    }
                    line_items.append(line_item)

            if line_items:

                checkout_session=stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse("success")),
                    cancel_url=request.build_absolute_uri(reverse('cancel'))

                )
                return redirect(checkout_session.url,code=303)


def success(request):
    cart_items=cartitem.objects.all()

    for cart_item in cart_items:
        product=cart_item.book
        if product.quantity>=cart_item.quantity:
            product.quantity=cart_item.quantity
            product.save()

    cart_item.delete()

    return render(request,'user/success.html')

def cancel(request):

    return render(request,'user/cancel.html')