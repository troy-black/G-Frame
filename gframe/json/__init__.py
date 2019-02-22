import json
import os

import gframe

from pkg_resources import resource_string
from pathlib import Path


class Json:
    def __init__(
            self,
            module_name: str,
            json_name='',
            local_path=os.path.join(str(Path.home()), gframe.dist_name),
            load=True,
    ):
        self.module_name = module_name
        if json_name == '':
            json_name = module_name.split('.')[-1] + '.json'
        self.json_name = json_name
        self.local_path = local_path
        self.data = {}
        if load:
            self.load()

    def load(self):
        if os.path.exists(self.get_local_json_path()):
            self.load_json_from_file(self.get_local_json_path())
        else:
            self.load_json_from_resource()

    def load_json_from_resource(self):
        self.save_data(self.load_string())

    def load_string(self) -> str:
        return str(resource_string(self.module_name, self.json_name), 'utf-8')

    def load_json_from_file(self, local_json_path: str):
        with open(local_json_path, 'r') as file:
            self.save_data(file.read())

    def save_data(self, json_data: str):
        self.data = json.loads(json_data)
        self.save()

    def save(self):
        if not os.path.isdir(self.get_local_path()):
            os.makedirs(self.get_local_path())
        with open(self.get_local_json_path(), 'w') as file:
            json.dump(self.data, file)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def get_local_json_path(self) -> str:
        return os.path.join(
                str(Path.home()),
                self.local_path,
                self.json_name,
        )

    def get_local_path(self) -> str:
        return os.path.join(
                str(Path.home()),
                self.local_path,
        )

    def remove_local_file(self):
        if self.local_file_exists:
            os.remove(self.get_local_json_path())

    def local_file_exists(self):
        return os.path.isfile(self.get_local_json_path())
