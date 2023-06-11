from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    """
    :param request: user Http reqeust to reach main page
    :return: Project main page
    """
    return render(request, "mainpage.html")
