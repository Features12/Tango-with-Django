from django.shortcuts import render


def index(request):
    context_dict = {'boldmessage': "Hello Inna"}
    return render(request, 'index.html', context_dict)