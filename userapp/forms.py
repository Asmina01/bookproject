

from django import forms
from newapp.models import Book,Author

class Authorform(forms.ModelForm):

    class Meta:

        model=Author
        fields=["name"]

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter the name'}),

        }

class Bookform(forms.ModelForm):

    class Meta:

        model=Book
        fields="__all__"

        widgets={
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'enter the book name'}),
            'author': forms.Select(attrs={'class': 'form-control', 'placeholder': 'enter the book author'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'enter the book price'})
        }



