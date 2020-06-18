from rest_framework import serializers
from .models import Project, Resource

# class FileSerializer(serializers.Serializer):
#     file = serializers.FileField()

# class MaskSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Mask
#         fields = ('no_mask', 'feather', 'mode', 'band', 'fill_value', 
#                     'threshold', 'hole_size', 'white_fill', 'no_data')


    # def __init__(self, *args, **kwargs):

    #     print("yes")
    #     print(kwargs)

    #     super().__init__(*args, **kwargs)

        # Don't pass the 'no_mask' arg up to the superclass
        # no_mask = kwargs.pop('no_mask', None)

        # Instantiate the superclass normally
        # super(MaskSerializer, self).__init__(*args, **kwargs)

        # if no_mask:
        #     self.fields = { 'no_mask': 1 }
            # self.fields.pop(field_name)

    # def __init__(self, *args, **kwargs):

    #     print(args)
    #     print(kwargs)
    #     print(self.data)
    #     print(self.fields['no_mask'] == True)
    #     print(self.fields['no_mask'] == False)
    #     print(self.fields['no_mask'] == 0)
    #     print(self.fields['no_mask'] == 1)
    #     print(self.fields['no_mask'] == 'True')
    #     print(self.fields['no_mask'] == 'False')
    #     print(self.fields['no_mask'] == '0')
    #     print(self.fields['no_mask'] == '1')
    #     if self.fields['no_mask'] == True:
            # self.fields = { 'no_mask': 1 }
    #         del self.fields['feather']
    #         del self.fields['mode']
    #         del self.fields['band']
    #         del self.fields['fill_value']
    #         del self.fields['threshold']
    #         del self.fields['hole_size']
    #         del self.fields['white_fill']
    #         del self.fields['no_data']

    #     super().__init__(*args, **kwargs)

class ResourceSerializer(serializers.ModelSerializer):
    # thumbnail = FileSerializer()
    takenAt = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    # mask = MaskSerializer()
    
    class Meta:
        model = Resource
        fields = ('name', 'version', 'extent', 'thumbnail', 'takenAt', 'level', 'resolution')
        # depth = 1
    
    # def __init__(self, *args, **kwargs):
    #     # Don't pass the 'mask' arg up to the superclass
    #     mask = kwargs.pop('mask', None)

    #     # Instantiate the superclass normally
    #     super(ResourceSerializer, self).__init__(*args, **kwargs)

    #     if mask:
    #         # Drop any fields that are not specified in the `mask` argument.
    #         self.fields.push(field_name)

    # def get_mask(self, obj):
    #     return MaskSerializer(obj.mask.all(), obj.mask.no_mask).data

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('name', 'version', 'resources')
        depth = 1