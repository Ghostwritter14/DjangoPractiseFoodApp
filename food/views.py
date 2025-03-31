from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at index.")

def item(request):
    return HttpResponse("Hello, world. You're at item.")