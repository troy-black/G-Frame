import json
import os
from pathlib import Path


class Json:
    def __init__(
            self,
            local_file=__file__,
            json_name='',
            load=True,
    ):
        self.local_path = str(os.path.dirname(os.path.realpath(local_file)))
        if json_name == '':
            json_name = os.path.basename(self.local_path) + '.json'
        self.json_name = json_name
        self.data = {}
        if load:
            self.load()

    def load(self):
        self.load_json_from_file(self.get_local_json_path())

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
                self.get_local_path(),
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

    def local_file_exists(self) -> bool:
        return os.path.isfile(self.get_local_json_path())
