import os


class ReadFile:
    def __init__(self, file_name):
        if os.path.isfile(file_name):
            self.file_name = file_name
        else:
            raise ValueError(f"Can not open {file_name}.")

    def get_content(self):
        content = []
        with open(self.file_name, encoding='utf-8') as file:
            for row in file:
                if isinstance(row, str):
                    content.append(row)
                else:
                    raise ValueError(f"File {self.file_name} content is not text.")
        return content


if __name__ == '__main__':
    file = ReadFile(".\screen_layout.txt")
    print(file.get_content())
