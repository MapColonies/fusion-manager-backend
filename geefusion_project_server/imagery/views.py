import os
import json
from geefusion_project_server.settings import BASE_DIR
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .models import Resource, Project
from .serializers import ProjectSerializer, ResourceSerializer
from datetime import datetime
from utils.extract.extract_project import get_project, get_project_versions
from utils.extract.extract_resource import get_resource, get_resource_versions, get_resource_image
from utils.search import get_all_in_directory, get_all_projects_by_name_in_directory_tree, get_all_resources_by_name_in_directory_tree
from config.gee_paths import get_imagery_projects_path, get_imagery_resources_path
from utils.constants.extensions import get_project_extension
from utils.path import change_root_dir, combine_to_path
from utils.constants.extensions import get_resource_extension, get_project_extension
from utils.constants.query_info import get_query_info
from utils.request import get_request_parameters
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.template import loader

IMAGERY_PROJECT_PATH = get_imagery_projects_path()
IMAGERY_RESOURCE_PATH = get_imagery_resources_path()
MODEL_TYPE = 'Imagery'

@api_view(['GET'])
def home(request):
    return HttpResponse('<h1>Projects home view</h1>')

@api_view(['GET'])
def about(request):
    return HttpResponse('<h1>About</h1>')

def search(request, model):

    # Get query info
    query_info = get_query_info(['name'], [True], model)

    # Extract query parameters
    query_parametes, error_message = get_request_parameters(request, query_info)
    if error_message != '': return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    name = query_parametes[0]

    # Get results matching given name
    if model == Resource:
        path = get_imagery_resources_path()
        matching_resources = get_all_resources_by_name_in_directory_tree(path, MODEL_TYPE, name)
        json_name = 'resources'
    else:
        path = get_imagery_projects_path()
        matching_resources = get_all_projects_by_name_in_directory_tree(path, MODEL_TYPE, name)
        json_name = 'projects'

    return Response({f'{json_name}': matching_resources})

@api_view(['GET'])
def resources(request):
    path = IMAGERY_RESOURCE_PATH + request.GET.get('path', '')
    results = get_all_in_directory(path, Resource, MODEL_TYPE)
    return Response(results)

@api_view(['GET'])
def resource(request):
    
    # Get query info
    query_info = get_query_info(['name', 'path', 'version'], [True, False, False], Resource)

    # Extract query parameters
    query_parametes, error_message = get_request_parameters(request, query_info)
    if error_message != '': return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    resource_name, resource_path, resource_version = query_parametes
    
    # Build full path
    # if resource_path != '' and not resource_path.endswith('/'): resource_path += '/'
    # resource_path = f'{IMAGERY_RESOURCE_PATH}{resource_path}{resource_name}{get_resource_extension()}'
    filename = f'{resource_name}{get_resource_extension()}'
    resource_path = combine_to_path(IMAGERY_RESOURCE_PATH, resource_path, filename)

    if resource_version == 'latest':
        resource, _, error_message = get_resource(resource_path, name=resource_name)
    else:
        resource, _, error_message = get_resource(resource_path, name=resource_name, version=int(resource_version))
    
    if error_message != '':
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)
   
    versions = None if resource_version != 'latest' else get_resource_versions(resource_path, resource_name)
    
    serialized = ResourceSerializer(resource)
    data = serialized.data
    return Response(data) if not versions else Response({'versions': versions, 'latest': data})

@api_view(['GET'])
def resource_image(request):

    # Get query info
    query_info = get_query_info(['name', 'path', 'version'], [True, False, True], Resource)

    # Extract query parameters
    query_parametes, error_message = get_request_parameters(request, query_info)
    if error_message != '': return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    resource_name, resource_path, resource_version = query_parametes

    # Build full path
    # if resource_path != '' and not resource_path.endswith('/'): resource_path += '/'
    # resource_path = f'{IMAGERY_RESOURCE_PATH}{resource_path}{resource_name}{get_resource_extension()}'
    filename = f'{resource_name}{get_resource_extension()}'
    resource_path = combine_to_path(IMAGERY_RESOURCE_PATH, resource_path, filename)

    # Get image path in static directory
    image_path, error_message = get_resource_image(resource_path, resource_name, resource_version)
    if error_message != '':
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)
    
    # Get image absolute path
    image_path = BASE_DIR + '/' + str(image_path)
    with open(image_path, 'rb') as image:
        return HttpResponse(image.read(), content_type='image/jpeg')

@api_view(['GET'])
def resource_search(request):
    return search(request, Resource)

@api_view(['GET'])
def projects(request):
    path = IMAGERY_PROJECT_PATH + request.GET.get('path', '')
    results = get_all_in_directory(path, Project, MODEL_TYPE)
    return Response(results)

@api_view(['GET'])
def project(request):

    # Get query info
    query_info = get_query_info(['name', 'path', 'version'], [True, False, False], Resource)

    # Extract query parameters
    query_parametes, error_message = get_request_parameters(request, query_info)
    if error_message != '': return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    project_name, project_path, project_version = query_parametes

    # Build full path
    # if project_path != '' and not project_path.endswith('/'): project_path += '/'
    # project_path = f'{IMAGERY_PROJECT_PATH}{project_path}{project_name}{get_project_extension()}'
    filename = f'{project_name}{get_project_extension()}'
    project_path = combine_to_path(IMAGERY_PROJECT_PATH, project_path, filename)
    
    if project_version == 'latest':
        project, error_message = get_project(project_path, project_name)
    else:
        project, error_message = get_project(project_path, project_name, int(project_version))

    if error_message != '':
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)

    versions = None if project_version != 'latest' else get_project_versions(project_path, project_name)
    serialized = ProjectSerializer(project)
    data = serialized.data

    if project.version == 0: project.delete()
    return Response(data) if not versions else Response({'versions': versions, 'latest': data})

@api_view(['GET'])
def project_search(request):
    return search(request, Project)