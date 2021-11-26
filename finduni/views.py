from django.shortcuts import render
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'index.html', {})


def colprob(request):
    return render(request, 'colprob.html', {})


def predcol(request):
    return render(request, 'predcol.html', {})


def convertgpa(request):
    return render(request, 'convertgpa.html', {})


def contact(request):
    return render(request, 'contacts.html', {})


def ind_test(request):
    return render(request, 'ind_tests.html', {})


def ind_college(request):
    return render(request, 'ind_college.html', {})
