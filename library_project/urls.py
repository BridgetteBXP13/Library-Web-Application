"""library_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from library_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name=''),
    path('std/', views.std, name='std'),
	path('bor/', views.bor, name='bor'),
    path('results/', views.results, name= 'results'),
    path('search/', views.search, name='search'),
    path('show_book/<book_id>', views.show_book, name='show-book'),
    path('checkout/<isbn>/<cID>', views.checkout, name='checkout'),
    path('checkin-get/', views.checkin_get, name='chin-get'),
    path('checkin-page/<isbn>/<cardid>', views.checkin_page, name='chin-page'),
    path('view/', views.view, name='view'),
    path('bor-already-exists/', views.bor_already_exist, name='bor-already-exists'),
    path('borsearch/', views.borsearch, name='borsearch'),
    path('borresults/', views.borresults, name='borresults'),
    path('show-borrower/<card_id>', views.show_borrower, name='show-borrower'),
    path('show-borrower/edit/<card_id>', views.edit_borrower, name='edit-borrower'),
    path('pay-fine/<loan_id>/<cID>', views.checkout, name='pay-fine'),
]


