from django.shortcuts import render


def homepage(request):
    return render(request, 'lmn/home.html')


def logout(request):
    return render(request, 'lmn/logout.html')
