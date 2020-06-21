import os
from unittest.mock import patch
with patch.dict('os.environ', { 'FUSION_PATH': '/'.join([os.path.dirname(os.path.abspath(__file__)), 'test_files', 'fusion/']) }):
    from django.test import TestCase, Client
    from django.urls import reverse, resolve
    # from imagery.models import Project, Resource, Mask
    from imagery.views import projects, resources, project, resource
import json

# Create your tests here.
class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()
        self.test_files_path = '/'.join([os.path.dirname(os.path.abspath(__file__)), 'test_files', 'fusion'])


    def test_resources(self):

        url = reverse('imagery-resources')
        self.assertEquals(resolve(url).func, resources)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'BlueMarble')
        self.assertContains(response, 'SFBayAreaLanSat_20021010')
        self.assertContains(response, 'SFHighResInset_20061010')
        self.assertContains(response, 'i3_15Meter_20041010')
    

    def test_resource(self):
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


    def test_projects(self):

        url = reverse('imagery-projects')
        self.assertEquals(resolve(url).func, projects)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'SFBayArea')
    
    
    def test_project(self):
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