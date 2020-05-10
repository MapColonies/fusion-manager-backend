from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Resource
from datetime import datetime

def home(request):
    return HttpResponse('<h1>Projects home view</h1>')

def about(request):
    return HttpResponse('<h1>About</h1>')

def resource(request):
    temp = Resource(name='test', version='1', extent='extent', takenAt=datetime.now(), resolution='1000x1000')
    temp_serialized = serializers.serialize('json', [temp, ])
    return HttpResponse(temp_serialized, content_type="application/json")