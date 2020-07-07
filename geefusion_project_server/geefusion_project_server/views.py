from django.http import HttpResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def home(request):
    return HttpResponse('<h1>Homepage</h1>')