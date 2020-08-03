import os

def get_assets_path():
    
    return os.environ.get('FUSION_PATH', f'{os.sep}gevol{os.sep}fusion{os.sep}') + f'assets{os.sep}'

def get_imagery_resources_path():

    return get_assets_path() + f'Resources{os.sep}Imagery{os.sep}'

def get_imagery_projects_path():

    return get_assets_path() + f'Projects{os.sep}Imagery{os.sep}'