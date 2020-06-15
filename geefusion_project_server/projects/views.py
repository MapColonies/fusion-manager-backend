from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Resource
from .serializers import ProjectSerializer, ResourceSerializer
from datetime import datetime
import os
import json
from .extract_project import get_project
from .extract_resource import get_resource, get_resource_by_name
from .gee_paths import get_imagery_projects_path
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template import loader

# with open("projects/config.json") as file:
#     ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"
# PROJECTS_PATH = ASSETS_PATH + "Projects/"
# RESOURCE_PATH = ASSETS_PATH + "Resources/"
IMAGERY_PATH = get_imagery_projects_path()

@api_view(['GET'])
def home(request):
    return HttpResponse('<h1>Projects home view</h1>')

@api_view(['GET'])
def about(request):
    return HttpResponse('<h1>About</h1>')

@api_view(['GET'])
def resource(request):
    
    resource_name = request.GET.get('name', 'bad')
    resource_version = int(request.GET.get('version', '-1'))

    if resource_name == 'bad':
        return Response("Resource name wasn't provided")
    
    if resource_version == -1:
        return Response("Resource version wasn't provided")

    # resource = get_resource('/opt/google/share/tutorials/fusion/assets/Resources/Imagery/BlueMarble.kiasset/', 1)
    resource, error_message = get_resource_by_name(resource_name, resource_version)

    if error_message != "":
        return Response(error_message)
    
    # TODO: Check that image is serverd correctly
    serialized = ResourceSerializer(resource)
    return Response(serialized.data)
    # return Response(resource.thumbnail)

    # temp = {
    #     "data": serialized.data
    # }

    # template = loader.get_template('test.html')
    # return HttpResponse(template.render(temp, request))

@api_view(['GET'])
def project(request):
    # temp = Resource(name='test', version='1', extent='extent', thumbnail=Image.imread("/opt/google/share/tutorials/fusion/assets/Resources/Imagery/BlueMarble.kiasset/product.kia/ver001/preview.png"), takenAt=datetime.now(), resolution='1000x1000')
    # temp_serialized = serializers.serialize('json', [temp, ])
    # with open("/opt/google/share/tutorials/fusion/assets/Resources/Imagery/BlueMarble.kiasset/product.kia/ver001/preview.png", "rb") as image:
    # return HttpResponse(temp_serialized, content_type="application/json")

    project_name = request.GET.get('name', 'bad')
    project_version = int(request.GET.get('version', ''))

    project, error_message = get_project(IMAGERY_PATH + project_name, project_version)

    if error_message != "":
        return Response(error_message)

    # serialized = serializers.serialize('json', [get_project(IMAGERY_PATH + projects[0], 1), ])
    serialized = ProjectSerializer(project)
    # return HttpResponse(serialized, content_type="application/json")
    return Response(serialized.data)

# def JSONResponse(HttpResponse):

#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)