from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response


def timesofind(request):
    return render_to_response('home.html')