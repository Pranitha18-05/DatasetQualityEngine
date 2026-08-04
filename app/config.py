import yaml


class Config:

    def __init__(self, path="config.yaml"):

        with open(path, "r") as file:

            self.data = yaml.safe_load(file)

    def get(self, *keys):

        value = self.data

        for key in keys:

            value = value[key]

        return value