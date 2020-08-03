import os
from unittest.mock import patch

from django.test import TestCase

from imagery.models import Project, Resource
from utils.constants.extensions import (get_project_extension,
                                        get_resource_extension)
from utils.path import (cd_path_n_times, combine_to_path,
                        get_file_name_from_path, get_path_suffix)

FUSION_PATH = os.sep.join([os.path.dirname(os.path.abspath(__file__)), 'test_files', f'fusion{os.sep}'])
with patch.dict('os.environ', { 'FUSION_PATH': FUSION_PATH }):
    from utils.search import (exists_with_version, get_versions, get_all_in_directory, 
                            get_all_projects_by_name_in_directory_tree, get_all_resources_by_name_in_directory_tree)

class TestPathUtils(TestCase):
    
    def setUp(self):
        self.test_path = os.sep.join(['level1', 'level2', 'level3', 'level4.txt'])


    def test_get_path_suffix(self):
        suffix = get_path_suffix(self.test_path)
        self.assertEquals(suffix, 'level4.txt')
    

    def test_get_file_name_from_path(self):
        file_name = get_file_name_from_path(self.test_path)
        self.assertEquals(file_name, 'level4')
    

    def test_cd_path_n_times(self):

        path = self.test_path

        result = cd_path_n_times(path)
        self.assertEquals(result, os.sep.join(['level1', 'level2', 'level3']))

        result = cd_path_n_times(path, 1)
        self.assertEquals(result, os.sep.join(['level1', 'level2', 'level3']))

        result = cd_path_n_times(path, 2)
        self.assertEquals(result, os.sep.join(['level1', 'level2']))

        result = cd_path_n_times(path, 3)
        self.assertEquals(result, 'level1')


class TestSearch(TestCase):

    def setUp(self):
        self.projects_path = combine_to_path(FUSION_PATH, 'assets', 'Projects', 'Imagery')
        self.resources_path = combine_to_path(FUSION_PATH, 'assets', 'Resources', 'Imagery')
        self.SFBayArea_project = combine_to_path(self.projects_path, 'SFBayArea.kiproject')
        self.BlueMarble_resource = combine_to_path(self.resources_path, 'BlueMarble.kiasset')

    def test_exists_with_version(self):

        ans, error = exists_with_version(self.SFBayArea_project, 1)
        self.assertEquals(ans, True)

        ans, error = exists_with_version(self.SFBayArea_project, 2)
        self.assertEquals(ans, False)

        ans, error = exists_with_version(self.BlueMarble_resource, 1)
        self.assertEquals(ans, False)

        ans, error = exists_with_version(self.BlueMarble_resource, 2)
        self.assertEquals(ans, True)
    
    def test_get_versions(self):

        versions = get_versions(self.SFBayArea_project)
        self.assertEquals(versions, [1])

        versions = get_versions(self.BlueMarble_resource)
        self.assertEquals(versions, [2])

    def test_get_all_projects_in_directory(self):
        projects = get_all_in_directory(self.projects_path, Project, 'Imagery')
        self.assertEquals(projects['projects'], ['SFBayArea'])
    
    def get_all_resources_in_directory(self):
        resources = get_all_in_directory(self.projects_path, Resource, 'Imagery')
        self.assertCountEqual(resources['resources'], ['BlueMarble', 'i3_15Meter_20041010', 'SFBayAreaLanSat_20021010', 'SFHighResInset_20061010'])

    def test_os_path_join(self):
        first = f'{os.sep}test{os.sep}'
        second = f'path{os.sep}'
        third = f'{os.sep}combine'
        self.assertEqual(os.path.join(os.sep, 'test', 'path', 'combine'), combine_to_path(first, second, third))
    
    def test_get_all_by_name_in_directory_tree(self):
        
        root_path = os.path.join(self.resources_path, 'hello', 'my')
        model_type = 'Imagery'
        name = 'BlueMarble'

        resources = get_all_resources_by_name_in_directory_tree(root_path, model_type, name)
        self.assertIn(os.path.join(os.sep, 'hello', 'my', name), resources)
