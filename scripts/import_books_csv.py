import csv

from library_app.models import Book, Authors, Book_Authors

def run():
    fhand = open('books.csv', encoding="UTF-8")
    reader = csv.reader(fhand, delimiter='\t')

    Book.objects.all().delete()
    Authors.objects.all().delete()
    Book_Authors.objects.all().delete()


    next(reader)
    
    for row in reader:
        book, created = Book.objects.get_or_create(Isbn=row[0], Title=row[2])

        authors = row[3].split(",")
        for x in authors:
            author, created = Authors.objects.get_or_create(Name=x)
            book_author, created = Book_Authors.objects.get_or_create(Author_id=author, Isbn=book)


            
