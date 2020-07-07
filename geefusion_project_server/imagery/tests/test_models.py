from django.test import TestCase
from imagery.models import Project, Resource, Mask

# Create your tests here.
class TestProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        
        mask = Mask.objects.create(no_mask=1,
            feather=100,
            mode='',
            band=0,
            fill_value=0, 
            threshold=0,
            hole_size=0,
            white_fill=0,
            no_data=None
        )

        resource = Resource.objects.create(
            name='test_resource', 
            version=1, path='/', 
            extent='453x3242', 
            takenAt='2020-03-03T00:00:00Z', 
            level='4', 
            resolution='5000m/px', 
            mask=mask
        )

        cls.project = Project.objects.create(name='test_project', version=1, path='/')

        cls.project.resources.add(resource)


    def test_resource_associated_to_project(self):

        self.assertEquals(self.project.name, 'test_project')

        resource = self.project.resources.get(name='test_resource')
        self.assertEquals(resource.name, 'test_resource')
    

    def test_mask_of_resource_associated_to_project(self):

        self.assertEquals(self.project.name, 'test_project')

        resource = self.project.resources.get(name='test_resource')
        mask = resource.mask

        self.assertEquals(mask.feather, 100)