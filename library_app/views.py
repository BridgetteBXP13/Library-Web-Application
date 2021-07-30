from django.shortcuts import render, redirect
from django.db.models import Q
from library_app.forms import BookForm, AuthorsForm, Book_AuthorsForm, BorrowerForm, BookLoansForm, FinesForm
from library_app.models import Book, Authors, Book_Authors, Borrower, Book_Loans, Fines
import logging
from datetime import datetime
from django.db.models.aggregates import Count
from django.db.models.fields import DateField
from django.utils import datetime_safe
from datetime import timedelta



logger = logging.getLogger("mylogger")

def std(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        authorForm = AuthorsForm(request.POST)
        
        if form.is_valid():
            
            new_book = form.save()
            book = Book.objects.get(Isbn=new_book.Isbn, Title=new_book.Title)
            
            new_author = authorForm.save(commit=False)
            
            authors = new_author.Name.split(",")
            for x in authors:

                new_author.Name = x
                new_author = authorForm.save(commit=False)
                author, created = Authors.objects.get_or_create(Name=x)
                new_book_author, created = Book_Authors.objects.get_or_create(Author_id=author, Isbn=book)
            authorForm.save_m2m()
            

            return redirect('/view')
    else:
        form = BookForm()
        authorForm = AuthorsForm()
        book_authorForm = Book_Authors()
        

    return render(request, 'index.html',{'form':form, 'authorForm':authorForm})

def bor(request):
    if request.method == "POST":
        form = BorrowerForm(request.POST)
        
        if form.is_valid():
            try:
                form.save()
                return redirect('/view')
            except:
                pass
    else:
        print(BookForm.errors)
        form = BorrowerForm()
    return render(request, 'Borrower.html',{'form':form})

def home_view(request, *args, **kwargs):
    return render(request, 'home.html',{})
    
def view(request, *args, **kwargs):
    return render(request, 'view.html',{})

def results(request):
    if request.method == "POST":
        searched = request.POST['searched']
        titles = Book_Authors.objects.filter(Q(Isbn__Title__icontains=searched) | Q(Author_id__Name__icontains=searched))
        titles_list = list(titles)
        x=0
        for title in titles_list:
            while x<(len(titles_list)-1):

                if titles_list[x].Isbn == titles_list[x+1].Isbn:

                    titles_list[x].Author_id.Name = (titles_list[x].Author_id.Name + ", " + titles_list[x+1].Author_id.Name)
                    titles_list.remove(titles_list[x+1])
                    x=x-1
                x=x+1

        return render(request, 'search-results.html', {'searched':searched, 'titles':titles, 'titles_list':titles_list})

    else:
        return render(request, 'search-results.html', {}) 


def borresults(request):
    if request.method == "POST":
        searched = request.POST['searched']
        borrowers = Borrower.objects.filter(Q(Name__icontains=searched) | Q(Card_id__icontains=searched) | Q(Phone__icontains=searched) | Q(Ssn__icontains=searched))
      
        return render(request, 'search-borrower-results.html', {'searched':searched, 'borrowers':borrowers})

    else:
        return render(request, 'search-borrower-results.html', {}) 

def search(request):
    return render(request, 'search-page.html', {}) 

def borsearch(request):
    return render(request, 'search-borrower.html', {}) 
def show_book(request, book_id):
    book = Book_Authors.objects.get(pk = book_id)
    x = book.Isbn.Isbn
    bookStat = Book_Loans.objects.filter(Isbn__Isbn=x, Date_in__isnull=True)
    bCount = bookStat.count()
    if request.method == "GET":
        return render(request, 'show-book.html', {'book': book, 'bookStat': bookStat, 'bCount': bCount})
    else: 
        cid = request.POST['cID']
        borrower = Borrower.objects.filter(Card_id=cid)
        idExist = borrower.count()

        loans = Book_Loans.objects.filter(Card_id=cid)
        booksout = loans.count()

        if idExist != 0 and booksout < 3 and bCount == 0:
            return redirect(f'/checkout/{book.Isbn.Isbn}/{cid}')
        else:
            return render(request, 'show-book.html', {'book': book, 'bookStat': bookStat, 'bCount': bCount, 'idExist' : idExist, 'booksout' : booksout })


def checkout(request, isbn, cID):
    
    formdone = False
    book = Book.objects.get(Isbn = isbn)
    cardID = cID

    isbnNum = book.Isbn
    currdate = datetime_safe.date.today()
    nextdate = (datetime_safe.date.today() + timedelta(days=14))
    
    formDic = {'Isbn' : isbnNum, 'Card_id' : cardID, 'Date_out' : currdate, 'Due_Date' : nextdate}
    if request.method == "GET":
        form = BookLoansForm(initial=formDic)   

        return render(request, 'checkout.html', {'formdone' : formdone, 'cardID': cardID, 'cID' : cID, 'book' : book, 'form' : form, 'currdate' : currdate, 'nextdate' : nextdate})

    else:

        formdone = True
        form = BookLoansForm(request.POST)
        if form.is_valid():
            #try:
                form.save()
                return render(request, 'checkout.html', {'form':form, 'formdone' : formdone})
           #except:
            #    logger.info("Somehow I made it here and broke")
             #   pass
        else:
            form = BookLoansForm(initial=formDic)
            formdone = False
            formgood = False
            return render(request, 'checkout.html', {'formdone' : formdone, 'formgood' : formgood, 'cardID': cardID, 'cID' : cID, 'book' : book, 'form' : form, 'currdate' : currdate, 'nextdate' : nextdate})


def show_loan(request, card_id):
    borrower = Borrower.objects.get(Card_id = card_id)
    x = borrower.Card_id.Card_id
    borLoan = Book_Loans.objects.filter(Card_id = card_id)
    borLoanCount = borLoan.count()
    if request.method == "GET":
        return render(request, 'show-loan.html', {'borrower': borrower, 'borLoan': borLoan, 'borLoanCount': borLoanCount})
    else: 
        cid = request.POST['cID']
        bor = Borrower.objects.filter(Card_id=cid)
        idExist = borrower.count()

        loans = Book_Loans.objects.filter(Card_id=cid)
        booksout = loans.count()

        if idExist != 0 and borLoan == 0:
            return redirect(f'/pay-fine/{loans.Loan_id}/{cid}')
        else:
            return render(request, 'show-book.html', {'borrower': borrower, 'borLoan': borLoan, 'borLoanCount':borLoanCount, 'idExist' : idExist, 'booksout' : booksout })

def show_borrower(request, card_id):
    borrower = Borrower.objects.get(Card_id = card_id)
    x = borrower.Card_id
    borLoan = Book_Loans.objects.filter(Card_id = card_id)
    borLoanCount = borLoan.count()
    if request.method == "GET":
        return render(request, 'show-borrower.html', {'borrower': borrower, 'borLoan': borLoan, 'borLoanCount': borLoanCount})
    else:
        cid = request.POST['cID']
        bor = Borrower.objects.filter(Card_id=cid)
        idExist = borrower.count()
       
        loans = Book_Loans.objects.filter(Card_id=cid)
        booksout = loans.count()

        if idExist != 0 and borLoan == 0:
            return redirect(f'/pay-fine/{loans.Loan_id}/{cid}')
        else:
            return render(request, 'show-borrower.html', {'borrower': borrower, 'borLoan': borLoan, 'borLoanCount':borLoanCount, 'idExist' : idExist, 'booksout' : booksout })


# DUPLICATE OF CHECKOUT TO-DO!
def pay_fine(request, loan_id, cID):
    
    formdone = False
    book = Book.objects.get(Isbn = isbn)
    cardID = cID

    isbnNum = book.Isbn
    currdate = datetime_safe.date.today()
    nextdate = (datetime_safe.date.today() + timedelta(days=14))
    
    formDic = {'Isbn' : isbnNum, 'Card_id' : cardID, 'Date_out' : currdate, 'Due_Date' : nextdate}
    if request.method == "GET":
        form = BookLoansForm(initial=formDic)   

        return render(request, 'checkout.html', {'formdone' : formdone, 'cardID': cardID, 'cID' : cID, 'book' : book, 'form' : form, 'currdate' : currdate, 'nextdate' : nextdate})

    else:

        formdone = True
        form = BookLoansForm(request.POST)
        if form.is_valid():
            #try:
                form.save()
                return render(request, 'checkout.html', {'form':form, 'formdone' : formdone})
           #except:
            #    logger.info("Somehow I made it here and broke")
             #   pass
        else:
            form = BookLoansForm(initial=formDic)
            formdone = False
            formgood = False
            return render(request, 'checkout.html', {'formdone' : formdone, 'formgood' : formgood, 'cardID': cardID, 'cID' : cID, 'book' : book, 'form' : form, 'currdate' : currdate, 'nextdate' : nextdate})

def edit_borrower(request, card_id):
    instance = get_object_or_404(Borrower, pk=card_id)
    form = BorrowerForm(request.POST or None, instance=instance)
    logger.info(form)
    if form.is_valid():
        form.save()
        return redirect('view')
    else:
        logger.info("Invalid form")
        
    return render(request, 'edit-borrower.html', {'borrower': instance, 'form':form})

