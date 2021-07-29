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
from django.urls import include, path
from library_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name=''),
    path('std/', views.std, name='std'),
	path('bor/', views.bor, name='bor'),
    path('results/', views.results, name='results'),
    path('search/', views.search, name='search'),
    path('view/', views.view, name='view'),
    path('borsearch/', views.borsearch, name='borsearch'),
    path('borresults/', views.borresults, name='borresults'),
    path('show-book/<book_id>', views.show_book, name='show-book'),
    path('checkout/<isbn>/<cID>', views.checkout, name='checkout'),
    path('show-loan/<loan_id>', views.show_loan, name='show-loan'),
    path('show-borrower/<card_id>', views.show_borrower, name='show-borrower'),
    path('pay-fine/<loan_id>/<cID>', views.checkout, name='pay-fine'),
    path('show-borrower/edit/<card_id>', views.edit_borrower, name='edit-borrower'),
]
