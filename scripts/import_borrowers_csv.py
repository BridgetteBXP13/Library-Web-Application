import csv

from library_app.models import Borrower

def run():
    fhand = open('borrowers.csv')
    reader = csv.reader(fhand)

    Borrower.objects.all().delete()


    next(reader)
    
    for row in reader:
        try:
            obj, created = Borrower.objects.get_or_create(Card_id=('I'+'D'+row[8][7]+row[8][8]+row[8][10]+row[8][11]+row[8][12]+row[8][13]), Ssn=row[1], Name=row[2]+" "+row[3], Address=row[5]+", "+row[6]+", "+row[7], Phone=row[8])
        except:
            print("Same phone number with last 6 digits!!!")