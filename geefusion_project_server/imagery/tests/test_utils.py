import os
from unittest.mock import patch
from django.test import TestCase
from imagery.models import Resource, Project
from utils.constants.extensions import get_project_extension, get_resource_extension
from utils.path import get_file_name_from_path, get_path_suffix, cd_path_n_times, combine_to_path

FUSION_PATH = '/'.join([os.path.dirname(os.path.abspath(__file__)), 'test_files', 'fusion/'])
with patch.dict('os.environ', { 'FUSION_PATH': FUSION_PATH }):
    from utils.search import exists_with_version, get_versions, get_all_in_directory

class TestPathUtils(TestCase):

    def test_get_path_suffix(self):

        path = 'level1/level2/level3/level4.txt'
        suffix = get_path_suffix(path)

        self.assertEquals(suffix, 'level4.txt')
    

    def test_get_file_name_from_path(self):

        path = 'level1/level2/level3/level4.txt'
        file_name = get_file_name_from_path(path)

        self.assertEquals(file_name, 'level4')
    

    def test_cd_path_n_times(self):

        path = 'level1/level2/level3/level4.txt'

        result = cd_path_n_times(path)
        self.assertEquals(result, 'level1/level2/level3')

        result = cd_path_n_times(path, 1)
        self.assertEquals(result, 'level1/level2/level3')

        result = cd_path_n_times(path, 2)
        self.assertEquals(result, 'level1/level2')

        result = cd_path_n_times(path, 3)
        self.assertEquals(result, 'level1')


class TestSearch(TestCase):

    def setUp(self):
        self.projects_path = '/'.join([FUSION_PATH, 'assets', 'Projects', 'Imagery'])
        self.resources_path = '/'.join([FUSION_PATH, 'assets', 'Resources', 'Imagery'])
        self.SFBayArea_project = '/'.join([self.projects_path, 'SFBayArea.kiproject'])
        self.BlueMarble_resource = '/'.join([self.resources_path, 'BlueMarble.kiasset'])

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
    
    # def test_get_directory_in_directory_tree(self):

    #     project_extension = get_project_extension()
    #     resource_extension = get_resource_extension()

    #     directory = get_directory_in_directory_tree(self.projects_path, 'random', project_extension)
    #     self.assertEqual(directory, None)

    #     directory = get_directory_in_directory_tree(self.projects_path, 'SFBayArea', project_extension)
    #     self.assertEqual(directory, self.SFBayArea_project)

    #     directory = get_directory_in_directory_tree(self.resources_path, 'random', resource_extension)
    #     self.assertEqual(directory, None)

    #     directory = get_directory_in_directory_tree(self.resources_path, 'BlueMarble', resource_extension)
    #     self.assertEqual(directory, self.BlueMarble_resource)

    def test_os_path_join(self):
        first = "/test/"
        second = "path/"
        third ="/combine"
        self.assertEqual('/test/path/combine', combine_to_path(first, second, third))