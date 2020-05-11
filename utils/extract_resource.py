import json

with open("utils/config.json") as file:
    ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"


def extract_resource(path, version):
    # TODO
    print("TODO")