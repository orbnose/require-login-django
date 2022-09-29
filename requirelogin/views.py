from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound

# Create your views here.

def index(request):
    return HttpResponse('index page for ' + request.user.username)


def nested_redir(request, test_flag=False):
    return HttpResponse('nested page for '+ request.user.username)


def nested_forbidden(request, test_flag=False):
    if not request.user.is_superuser:
        return HttpResponseForbidden('forbidden')

    return HttpResponse('nested forbidden page for ' + request.user.username)
