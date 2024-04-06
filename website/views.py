from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def settings(request):
    return render(request, "settings.html")
