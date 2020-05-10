import json


class Configuration:
    base_dir = '/'

    def load_data(self, data):
        self.base_dir = data['base_dir']

    def load_file(self, input_path):
        data = {
            "base_dir": self.base_dir
        }

        try:
            with open(input_path) as json_file:
                data = json.load(json_file)
                self.load_data(data)
        except FileNotFoundError:
            with open(input_path, 'x') as file:
                json.dump(data, file)
