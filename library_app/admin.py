from django.contrib import admin
# Import our models
from library_app.models import Book
from library_app.models import Authors
from library_app.models import Book_Authors
from library_app.models import Borrower
from library_app.models import Book_Loans
from library_app.models import Fines

# Register your models here.
admin.site.register(Book)
admin.site.register(Authors)
admin.site.register(Book_Authors)
admin.site.register(Borrower)
admin.site.register(Book_Loans)
admin.site.register(Fines)