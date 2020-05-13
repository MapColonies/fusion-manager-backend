import json
from datetime import datetime
from xmlconverter import XMLConverter

with open("config.json") as file:
    ASSETS_PATH = json.load(file)["FUSION_PATH"] + "assets/"


def extract_resource(path, version):
    # TODO
    print("TODO")


def get_creation_time(path):
    json = XMLConverter.convert(path + "/khasset.xml")
    return datetime.strptime(json["meta"]["item"][2], '%Y-%m-%dT%H:%M:%SZ')