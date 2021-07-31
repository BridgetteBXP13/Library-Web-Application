from django.core import validators
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import DecimalField, PositiveBigIntegerField
from django.core.validators import RegexValidator
from datetime import datetime, timedelta

# BOOK
class Book(models.Model):
    Isbn = models.CharField(max_length=10, null=False, blank=False, primary_key=True, unique=True)
    Title = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'BOOK' # Just controls table name to make it BOOK and not library_app_book

# AUTHORS
class Authors(models.Model):
    Author_id = models.AutoField(null=False, blank=False, primary_key=True, unique=True)
    Name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    
    class Meta:
        db_table = 'AUTHORS'
        verbose_name_plural="Authors"

# BOOK_AUTHORS
class Book_Authors(models.Model):
    Book_Authors_id = models.AutoField(null=False, blank=False, primary_key=True, unique=True)
    Author_id = models.ForeignKey(Authors, on_delete=models.CASCADE, unique=False)
    Isbn = models.ForeignKey(Book, default='0000000001', on_delete=models.CASCADE, unique=False)

    class Meta:
        db_table = 'BOOK_AUTHORS'
        verbose_name_plural="Book_Authors"

# BORROWER
class Borrower(models.Model):
    Card_id = models.CharField(max_length=8, null=False, blank=True, primary_key=True, unique=True)
    Ssn = models.CharField(max_length=11, null=False, blank=False, validators=[RegexValidator(r'^[0-9]{3}[-]{1}[0-9]{2}[-]{1}[0-9]{4}$', 'Valid ssn is required! \nMust be in form: 123-45-6789')])
    Name = models.CharField(max_length=200, null=False, blank=False)
    Address = models.CharField(max_length=200, null=False, blank=False)
    Phone = models.CharField(max_length=14, null=False, blank=False, validators=[RegexValidator(r'^[(]{1}[0-9]{3}[)]{1}[ ]{1}[0-9]{3}[-]{1}[0-9]{4}$', 'Valid Phone number is required! \nMust be in form: (123) 456-7890')])

    def save(self, *args, **kwargs):
        if not self.Card_id:
            self.Card_id = ('I'+'D'+self.Phone[7]+self.Phone[8]+self.Phone[10]+self.Phone[11]+self.Phone[12]+self.Phone[13])
        super(Borrower, self).save(*args, **kwargs)
    class Meta:
        db_table = 'BORROWER'

# BOOK_LOANS
class Book_Loans(models.Model):
    Loan_id = models.AutoField(primary_key=True, blank=False, null=False)
    Isbn = models.ForeignKey(Book, default='0000000001', on_delete=models.CASCADE)
    Card_id = models.ForeignKey(Borrower, default="ID000000", on_delete=models.CASCADE)
    Date_out = models.DateField(auto_now=False, auto_now_add=False)
    Due_Date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.now()+timedelta(days=14))
    Date_in = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)

    class Meta:
        db_table = 'BOOK_LOANS'
        verbose_name_plural="Book_Loans"

# FINES
class Fines(models.Model):
    Loan_id = models.ForeignKey(Book_Loans, default=1, on_delete=models.CASCADE)
    Fine_amt = DecimalField(max_digits=3, decimal_places=2, null=False, blank=False, default=0)
    Paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        try:
            book_loan = Book_Loans.objects.get(Loan_id=self.Loan_id.Loan_id)
            if book_loan.Date_in == None:
                delta = datetime.now().date() - book_loan.Due_Date
            else:
                delta = book_loan.Date_in - book_loan.Due_Date
                
            if delta.days > 0:
                self.Fine_amt = (.25*delta.days)
            else:
                self.Fine_amt = 0
                self.Paid = True
        except:
            print("Given book loan id doesn't exist!")
        super(Fines, self).save(*args, **kwargs)

    class Meta:
        db_table = 'FINES'
        verbose_name_plural="Fines"