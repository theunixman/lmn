from django.shortcuts import render


def homepage(request):
    return render(request, 'lmn/home.html')


def logged_out(request):
    return render(request, 'lmn/logged_out.html')
