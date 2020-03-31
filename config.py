import json


class Configuration:
    base_dir = '/etc/nginx/conf.d/'

    def load_file(self, input_path):
        data = {
            "base_dir": self.base_dir
        }

        try:
            data = json.load(input_path)
        except FileNotFoundError:
            with open(input_path, 'w+') as file:
                json.dump(data, file)
