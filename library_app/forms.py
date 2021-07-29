from django import forms
from library_app.models import Book, Authors, Book_Authors, Borrower, Book_Loans, Fines

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

class AuthorsForm(forms.ModelForm):
    class Meta:
        model = Authors
        fields = "__all__"

class Book_AuthorsForm(forms.ModelForm):
    class Meta:
        model = Book_Authors
        fields = "__all__"

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = "__all__"

class BookLoansForm(forms.ModelForm):
    class Meta:
        model = Book_Loans
        fields = [
            'Isbn',
            'Card_id',
            'Date_out',
            'Due_Date'
        ]

class FinesForm(forms.ModelForm):
    class Meta:
        model = Fines
        fields = [
            'Paid',
        ]