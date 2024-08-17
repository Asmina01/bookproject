from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
from .forms import Authorform,Bookform
from django.contrib import messages,auth
from django.contrib.auth import login, authenticate

# Create your views here.

from .models import Book,Author,loginTable,UserProfile


    #def creatbook(request):

       #   books = Book.objects.all()
        #  if request.method=="POST":

            #  title=request.POST.get('title')
            #  price=request.POST.get('price')

            #  book=Book(title=title,price=price)
           #   book.save()

         # return render(request,'book.html',{'books':books})

def paginator(books, param):
    pass


def listview(request):

    books=Book.objects.all()

    paginator=Paginator(books,4)
    page_number=request.GET.get('page')


    try:
        page=paginator.get_page(page_number)

    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    return render(request,'admin/listview.html',{'books':books,'page':page})

def detailsview(request,book_id):

    book=Book.objects.get(id=book_id)

    return render(request,'admin/detailsview.html',{'book':book})

def updatebook(request,book_id):

    book=Book.objects.get(id=book_id)
    if request.method=="POST":
        form=Bookform(request.POST,files=request.FILES,instance=book)

        if form.is_valid():
            form.save()
            return redirect("booklist")
    else:
        form=Bookform(instance=book)


    return render(request,'admin/updatebook.html',{'form':form})


def deleteview(request,book_id):

    book=Book.objects.get(id=book_id)

    if request.method=="POST":
        book.delete()
        return redirect("booklist")


    return render(request,'admin/deleteview.html',{'book':book})

def deleteauthor(request,author_id):

    book=Author.objects.get(id=author_id)

    if request.method=="POST":
        book.delete()
        return redirect("authorlist")


    return render(request,'admin/deleteauthor.html',{'book':book})




def creatbook(request):

    books=Book.objects.all()

    if request.method=="POST":
        form=Bookform(request.POST,files=request.FILES)

        if form.is_valid():
            form.save()

            return redirect("booklist")
    else:
        form=Bookform()

    return render(request,"admin/book.html",{'form':form,'books':books})

def creatauthor(request):

    if request.method=="POST":
        form=Authorform(request.POST)

        if form.is_valid():
            form.save()

            return redirect("authorlist")
    else:
        form=Authorform

    return render(request,"admin/author.html",{"form":form})




def loginuser(request):

    if request.method=="POST":
        username=request.POST.get("username")
        password = request.POST.get("password")

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('userlistview')




    return render(request,'admin/login.html')


def search_book(request):
    query=None
    books=None

    if 'q' is request.GET:
        query=request.GET.get('q')
        books.objects.filter(Q(title__icontains=query))

    else:
        books=[]

    context={'books':books,'query':query}
    return render(request,'admin/search.html',context)





def logout(request):
    auth.logout(request)
    return redirect('login')

def listauthor(request):

    books=Author.objects.all()

    paginator=Paginator(books,10)
    pagenumber=request.GET.get('page')


    try:
        page=paginator.get_page(pagenumber)

    except EmptyPage:
        page=paginator.page(pagenumber.num_pages)

    return render(request,'admin/listauthor.html',{'books':books,'page':page})



def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # Check if passwords match
        if password != password1:
            messages.error(request, "Passwords do not match")
            return redirect('registration')

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('registration')

        # Create the user
        user = User.objects.create_user(username=username, password=password1)
        user.save()

        # Authenticate and log in the user
        user = authenticate(request, username=username, password=password1)
        if user is not None:
            login(request, user)
            return redirect('login')  # Redirect to user list view after logging in

    return render(request, 'admin/registration.html')


def loginpage(request):

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=loginTable.objects.filter(username=username,password=password,type='user').exists()
        try:
            if user is not None:
                user_details=loginTable.objects.get(username=username,password=password)
                user_name=user_details.username
                type=user_details.type

                if type=='user':
                    request.session['username']=user_name
                    return redirect('userindex')
                elif type=='admin':
                    request.session['username'] = user_name
                    return redirect('admin_index')
            else:
                messages.error(request,'invalid details')

        except:
            messages.error(request,'invalid')
    return render(request,'admin/login.html')



def admin_index(request):

    # Logic for the admin page
    return render(request, 'admin/index.html')

def userindex(request):
    # Logic for the user page
    return render(request, 'user/userindex.html')










