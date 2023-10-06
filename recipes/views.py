from django.shortcuts import render, HttpResponse


def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Matheus Cardoso'
    })
