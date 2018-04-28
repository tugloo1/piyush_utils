


BasicFuncs(object):
    @staticmethod
    def write_to_file(file_name: str, file_content: str, encoding='utf-8'):
        with open(file_name, 'w', encoding=encoding) as f:
            f.write(file_content)
