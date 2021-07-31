from datetime import datetime
from django.http.response import Http404
from django.db.models.aggregates import Count
from django.db.models.fields import DateField
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import datetime_safe
from datetime import timedelta
import logging
from django.shortcuts import get_object_or_404
from library_app.forms import BookForm, AuthorsForm, Book_AuthorsForm, BorrowerForm, BookLoansForm, FinesForm, BorrowerUpdateForm
from library_app.models import Book, Borrower, Authors, Book_Authors, Book_Loans, Fines

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
                new_borrower = form.save(commit=False)
                borrowers = Borrower.objects.filter(Q(Phone__iexact=new_borrower.Phone) | Q(Ssn__iexact=new_borrower.Ssn))
                if not borrowers:
                    form.save()
                    return redirect('/view')
                else:
                    raise Http404("Borrower with given phone or SSN already exists!")
            except:
                return redirect('/bor-already-exists')
                pass
    else:
        print(BookForm.errors)
        form = BorrowerForm()
    return render(request, 'Borrower.html',{'form':form})

def home(request):
    return render(request, 'home.html', {})

def view(request, *args, **kwargs):
    return render(request, 'view.html',{})

def bor_already_exist(request, *args, **kwargs):
    return render(request, 'bor-already-exists.html',{})

def results(request):
    if request.method == "POST":
        searched = request.POST['searched']
        titles = Book_Authors.objects.filter(Q(Isbn__Isbn__icontains=searched) | Q(Isbn__Title__icontains=searched) | Q(Author_id__Name__icontains=searched)).order_by('Isbn')
        titles_list = list(titles)
        x=0
        if searched != '':
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


def loanresults(request):
    if request.method == "POST":
        searched = request.POST['searched']
        loan = Book_Loans.objects.filter(Q(Isbn__Isbn__icontains=searched) | Q(Card_id__Card_id__icontains=searched) | Q(Card_id__Name__icontains=searched))

        return render(request, 'search-loan-results.html', {'loan' : loan, 'searched' : searched})

    else:
        return render(request, 'search-loan-results.html', {})
     


def search(request):
    return render(request, 'search-page.html', {}) 

def borsearch(request):
    return render(request, 'search-borrower.html', {}) 

def loansearch(request):
    return render(request, 'search-loan.html', {}) 

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

        loans = Book_Loans.objects.filter(Card_id=cid, Date_in__isnull=True)
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
            try:
                book_loan=form.save()
                book_loan.Due_Date = book_loan.Date_out + timedelta(days=14)
                book_loan.save()
                fines = Fines.objects.create(Loan_id=book_loan)
                return render(request, 'checkout.html', {'form':form, 'formdone' : formdone})
            except:
            #    logger.info("Somehow I made it here and broke")
                pass
        else:
            form = BookLoansForm(initial=formDic)
            formdone = False
            formgood = False
            return render(request, 'checkout.html', {'formdone' : formdone, 'formgood' : formgood, 'cardID': cardID, 'cID' : cID, 'book' : book, 'form' : form, 'currdate' : currdate, 'nextdate' : nextdate})

def show_loan(request, loan_id):
    borLoan = Book_Loans.objects.get(Loan_id = loan_id)
    borBook = Book.objects.get(Isbn=borLoan.Isbn.Isbn)
    borFine = Fines.objects.get(Loan_id = loan_id)
    borFine.save()
    x = borLoan.Card_id.Card_id
    borrower = Borrower.objects.get(Card_id = x)

    return render(request, 'show-loan.html', {'borLoan':borLoan,'borFine':borFine,'borBook':borBook, 'borrower':borrower})


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
        idExist = bor.count()
       
        loans = Book_Loans.objects.filter(Card_id=cid)
        booksout = loans.count()

        if idExist != 0 and borLoan == 0:
            return redirect(f'/pay-fine/{loans.Loan_id}/{cid}')
        else:
            return render(request, 'show-borrower.html', {'borrower': borrower, 'borLoan': borLoan, 'borLoanCount':borLoanCount, 'idExist' : idExist, 'booksout' : booksout })

def checkin_get(request):
    if request.method == 'GET':
        return render(request, 'checkin-get.html', {})


    else:
        isbn = request.POST['isbn']
        cid = request.POST['cardid']

        loan = Book_Loans.objects.filter(Isbn = isbn, Card_id = cid, Date_in__isnull=True)
        loanExist = loan.count()

        if loanExist > 0:
            return redirect(f'/checkin-page/{isbn}/{cid}')

        else:
            return render(request, 'checkin-get.html', {'loanExist' : loanExist})
            
def checkin_page(request, isbn, cardid):
    currdate = datetime_safe.date.today()
    loan = Book_Loans.objects.get(Isbn = isbn, Card_id = cardid, Date_in__isnull=True)
    loan.Date_in = currdate
    loan.save()
    return render(request, 'checkin-page.html', {})

def pay_fine(request, loan_id):
    fine = Fines.objects.get(Loan_id = loan_id)
    fine.Paid = True
    fine.save()
    return render(request, 'pay-fine.html', {'fine' : fine})

def edit_borrower(request, card_id):
    instance = get_object_or_404(Borrower, pk=card_id)
    old_instance = get_object_or_404(Borrower, pk=card_id)
    loan_instance = Book_Loans.objects.filter(Card_id=old_instance.Card_id)
    form = BorrowerForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        if instance.Phone != old_instance.Phone:
            loan_instance = Book_Loans.objects.filter(Card_id=old_instance.Card_id).update(Card_id=instance.Card_id)
                

            Borrower.objects.filter(Phone=old_instance.Phone).delete()
        return redirect('view')
        
    return render(request, 'edit-borrower.html', {'borrower': instance,'loan_instance':loan_instance, 'form':form})

def delbook(request, isbn):
    Book.objects.filter(Isbn = isbn).delete()
    return render(request, 'del-book.html', {})

def delbor(request, cardid):
    Borrower.objects.filter(Card_id = cardid).delete()
    return render(request, 'del-bor.html', {})