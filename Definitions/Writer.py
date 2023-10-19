class NullWriter:
    def write(self, string):
        pass


class ConsoleWriter(NullWriter):
    def write(self, string):
        print(string)


class FileWriter(NullWriter):
    def __init__(self, file_name):
        self.file = open(file_name, "w")
        self.text = ""
    
    def write(self, string):
        self.text += string
        if len(self.text) > 100:
            self.file.write(self.text)
            self.text = ""
