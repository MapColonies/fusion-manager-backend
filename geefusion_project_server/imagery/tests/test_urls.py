import os
from unittest.mock import patch

FUSION_PATH = os.sep.join([os.path.dirname(os.path.abspath(__file__)), 'test_files', f'fusion{os.sep}'])
with patch.dict('os.environ', { 'FUSION_PATH': FUSION_PATH }):
    from django.test import TestCase, Client
    from django.urls import reverse, resolve
    # from imagery.models import Project, Resource, Mask
    from imagery.views import projects, resources, project, resource, resource_search, project_search
import json

# Create your tests here.
class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()


    def test_resources(self):

        url = reverse('imagery-resources')
        self.assertEquals(resolve(url).func, resources)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        json_resources = json.loads(response.content)['resources']
        self.assertIn('BlueMarble', json_resources)
        self.assertIn('SFBayAreaLanSat_20021010', json_resources)
        self.assertIn('SFHighResInset_20061010', json_resources)
        self.assertIn('i3_15Meter_20041010', json_resources)
    

    def test_resource_exists(self):
        # Get url
        url = reverse('imagery-resource')

        # Check that url gives correct function
        self.assertEquals(resolve(url).func, resource)

        # Make request
        response = self.client.get(url, data={ 'name': 'BlueMarble' })
        self.assertEqual(response.status_code, 200)

        # Check resorce name
        self.assertEquals(
            json.loads(response.content)['latest']['name'], 
            'BlueMarble'
        )

        # Check resource versions
        self.assertEquals(
            json.loads(response.content)['versions'], 
            [2]
        )
    

    def test_resource_does_not_exist(self):
        # Get url
        url = reverse('imagery-resource')

        # Check that url gives correct function
        self.assertEquals(resolve(url).func, resource)

        # Make request
        response = self.client.get(url, data={ 
            'path': 'hello',
            'name': 'BlueMarble' 
        })
        self.assertEqual(response.status_code, 404)

        # Check response message
        self.assertEquals(
            json.loads(response.content), 
            "Does not exist"
        )


    def test_projects(self):

        url = reverse('imagery-projects')
        self.assertEquals(resolve(url).func, projects)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('SFBayArea', json.loads(response.content)['projects'])
    
    
    def test_project_exists(self):
        # Get url
        url = reverse('imagery-project')

        # Check that url gives correct function
        self.assertEquals(resolve(url).func, project)

        # Make request
        response = self.client.get(url, data={ 'name': 'SFBayArea' })

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Check project name
        self.assertEquals(
            json.loads(response.content)['latest']['name'], 
            'SFBayArea'
        )

        # Check project versions
        self.assertEquals(
            json.loads(response.content)['versions'], 
            [1]
        )
    
    
    def test_search_project(self):
        # Get url
        url = reverse('imagery-project-search')

        # Check that url gives correct function
        self.assertEquals(resolve(url).func, project_search)
        
        name = 'SFBayArea'

        # Make request
        response = self.client.get(url, data={ 'name': name })

        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check paths of projects by the name SFBayArea
        self.assertEquals(
            json.loads(response.content)['projects'], 
            [os.path.join(os.sep, 'hello', 'my', 'friend', name), os.path.join(os.sep, name)]
        )
    
    
    def test_search_resource(self):
        # Get url
        url = reverse('imagery-resource-search')

        # Check that url gives correct function
        self.assertEquals(resolve(url).func, resource_search)
        
        name = 'BlueMarble'

        # Make request
        response = self.client.get(url, data={ 'name': name })

        # Check response status code
        self.assertEqual(response.status_code, 200)
        
        # Check paths of resources by the name SFBayArea
        self.assertEquals(
            json.loads(response.content)['resources'], 
            [os.path.join(os.sep, 'hello', 'my', 'friend', name),
             os.path.join(os.sep, 'hello', 'my', name),
             os.path.join(os.sep, 'hello', name),
             os.path.join(os.sep, name)]
        )