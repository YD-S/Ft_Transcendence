from django.shortcuts import render


def generic(file: str):
    def view(request):
        return render(request, file)
    return view
