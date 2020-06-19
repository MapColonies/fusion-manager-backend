from rest_framework import serializers
from .models import Project, Resource, Mask
from utils.mask import mask_to_json

# class MaskSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Mask
#         fields = ('no_mask', 'feather', 'mode', 'band', 'fill_value', 
#                     'threshold', 'hole_size', 'white_fill', 'no_data')

class ResourceSerializer(serializers.ModelSerializer):
    takenAt = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    mask = serializers.SerializerMethodField()
    
    class Meta:
        model = Resource
        fields = ('name', 'version', 'extent', 'thumbnail', 'takenAt', 'level', 'resolution', 'mask')
        depth = 1
    
    def get_mask(self, obj):
        mask = obj.mask

        if mask.no_mask:
            return { 'no_mask': True }
        
        return {
            'feather': mask.feather,
            'mode': mask.mode,
            'band': mask.band,
            'fill_value': mask.fill_value,
            'threshold': mask.threshold,
            'hole_size': mask.hole_size,
            'white_fill': mask.white_fill,
            'no_data': mask.no_data
        }

class ProjectSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True)
    version = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'version', 'resources')
        depth = 2
    
    def get_version(self, obj):
        version = obj.version
        return version if version != 0 else None