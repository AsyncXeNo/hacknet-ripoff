from utils.logger import Logger


class File(object):
    def __init__(self, path, name: str, ext: str = None, content: str = ""):
        self.logger = Logger("game/file")

        self.path = path        
        self.name = name
        self.ext = ext
        self.content = content

    def read(self):
        return self.content

    def write(self, content: str):
        self.content = content

    def append(self, content: str):
        self.content += content

    def replace(self, old, new, count=None):
        if count == None:
            self.content.replace(old, new)
            return

        self.content.replace(old, new, count)

    def get_name(self):
        if self.ext:
            return f"{self.name}.{self.ext}"
        else:
            return self.name

    def set_name(self, fullname: str):
        oldname = self.get_name()
        
        if fullname == "":
            self.logger.log_error("Filename cannot be empty string.")
            raise Exception("Filename cannot be empty string.")

        fullname = fullname.split(".")
        if len(fullname) == 1:
            name = fullname[0]
            ext = None
        elif len(fullname) == 2:
            name = fullname[0]
            ext = fullname[-1]   
        else:
            name = "".join(fullname[:-1])
            ext = fullname(-1)
        
        self.name = name
        self.ext = ext

        self.logger.log_neutral(f"Changed file name from {oldname} to {self.get_name()}")