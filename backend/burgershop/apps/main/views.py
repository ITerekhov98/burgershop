from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse


def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'main/index.html')