from rest_framework import serializers
from .models import Project, Resource, Mask
from utils.mask import mask_to_json
from utils.path import change_root_dir
from utils.constants.extensions import get_project_extension, get_resource_extension

class ResourceSerializer(serializers.ModelSerializer):
    taken_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    mask = serializers.SerializerMethodField()
    search_path = serializers.SerializerMethodField()
    
    class Meta:
        model = Resource
        fields = ('name', 'version', 'search_path', 'extent', 'taken_at', 'level', 'resolution', 'mask')
        depth = 1
    
    def get_mask(self, obj):
        mask = obj.mask
        return mask_to_json(mask)
    
    def get_search_path(self, obj):
        extension = get_resource_extension()
        return change_root_dir(obj.path, 'Imagery')[:-len(extension)]

class ProjectSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True)
    version = serializers.SerializerMethodField()
    search_path = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'version', 'search_path', 'resources')
        depth = 2
    
    def get_version(self, obj):
        version = obj.version
        return version if version != 0 else None
    
    def get_search_path(self, obj):
        extension = get_project_extension()
        return change_root_dir(obj.path, 'Imagery')[:-len(extension)]