from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'layout.html', {})
