import json


class BasicFuncs(object):
    @staticmethod
    def write_to_file(file_name: str, file_content: str, encoding='utf-8'):
        with open(file_name, 'w', encoding=encoding) as f:
            f.write(file_content)

    @staticmethod
    def get_api_key_from_file(file_name: str, encoding='utf-8') -> str:
        with open(file_name, 'r', encoding=encoding) as f:
            file_content = f.read()
        first_line = file_content.splitlines()[0]
        api_key = first_line.lstrip().rstrip()
        return api_key

    @staticmethod
    def load_json_file(file_path: str) -> str:
        with open(file_path, 'r') as f:
            json_dict = json.loads(f.read())
        return json_dict
