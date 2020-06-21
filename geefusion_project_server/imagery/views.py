import os
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Resource
from .serializers import ProjectSerializer, ResourceSerializer
from datetime import datetime
from utils.extract.extract_project import get_project_by_name, get_project_versions
from utils.extract.extract_resource import get_resource, get_resource_by_name, get_resource_versions
from utils.search import get_all_projects_in_directory_tree, get_all_resources_in_directory_tree
from config.gee_paths import get_imagery_projects_path, get_imagery_resources_path
from utils.constants.extensions import get_project_extension
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template import loader

IMAGERY_PROJECT_PATH = get_imagery_projects_path()
IMAGERY_RESOURCE_PATH = get_imagery_resources_path()

@api_view(['GET'])
def home(request):
    return HttpResponse('<h1>Projects home view</h1>')

@api_view(['GET'])
def about(request):
    return HttpResponse('<h1>About</h1>')

@api_view(['GET'])
def resources(request):
    results = get_all_resources_in_directory_tree(IMAGERY_RESOURCE_PATH)
    return JsonResponse({'resources': results})

@api_view(['GET'])
def resource(request):
    
    resource_name = request.GET.get('name', 'bad')
    resource_version = request.GET.get('version', 'latest')

    if resource_name == 'bad':
        return Response("Resource name wasn't provided")

    if resource_version == 'latest':
        resource, mask, error_message = get_resource_by_name(resource_name)
    else:
        resource, mask, error_message = get_resource_by_name(resource_name, int(resource_version))
    
    if error_message != "":
        return Response(error_message)
    
    versions = None if resource_version != '' else get_resource_versions(resource_name)
    
    serialized = ResourceSerializer(resource)
    data = serialized.data
    return Response(data) if not versions else Response({'versions': versions, 'latest': data})

@api_view(['GET'])
def projects(request):

    results = get_all_projects_in_directory_tree(IMAGERY_PROJECT_PATH)
    return JsonResponse({'projects': results})

@api_view(['GET'])
def project(request):
    project_name = request.GET.get('name', 'bad')
    project_version = request.GET.get('version', 'latest')

    if project_name == 'bad':
        return Response("Project name wasn't provided")

    if project_version == 'latest':
        project, error_message = get_project_by_name(project_name)
    else:
        project, error_message = get_project_by_name(project_name, int(project_version))

    if error_message != "":
        return Response(error_message)

    versions = None if project_version != '' else get_project_versions(project_name)
    serialized = ProjectSerializer(project)
    data = serialized.data

    if project.version == 0: project.delete()
    return Response(data) if not versions else Response({'versions': versions, 'latest': data})