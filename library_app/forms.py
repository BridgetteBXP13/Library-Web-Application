from django import forms
from library_app.models import Book, Borrower, Book_Loans, Authors, Book_Authors, Fines

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
        fields = [
            'Card_id',
            'Ssn',
            'Name',
            'Address',
            'Phone'
        ]

            
class BookLoansForm(forms.ModelForm):
    class Meta:
        model = Book_Loans
        fields = [
            'Isbn',
            'Card_id',
            'Date_out',
        ]


class BorrowerUpdateForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = [
            'Ssn',
            'Name',
            'Address',
            'Phone'
        ]

class FinesForm(forms.ModelForm):
    class Meta:
        model = Fines
        fields = [
            'Paid',
        ]