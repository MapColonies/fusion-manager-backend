from django.test import TestCase
from utils.string_utils import get_file_name_from_path, get_path_suffix, cd_path_n_times

class TestStringUtils(TestCase):

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