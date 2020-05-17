from rest_framework import serializers
from .models import Project, Resource

# class FileSerializer(serializers.Serializer):
#     file = serializers.FileField()

class ResourceSerializer(serializers.ModelSerializer):
    # thumbnail = FileSerializer()
    takenAt = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    
    class Meta:
        model = Resource
        fields = ('name', 'version', 'extent', 'thumbnail', 'takenAt', 'level', 'resolution')

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('name', 'version', 'resources')
        depth = 1