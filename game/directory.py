from utils.logger import Logger


class Directory(object):
    def __init__(self, name: str):
        self.logger = Logger("game/directory/Directory")

        self.name = name
        self.parent = None

        self.contents = {
            "files": [],
            "dirs": []
        }

        self.logger.log_neutral(f"Created a directory named {self.get_name()}")

    def tree(self):
        return self.bfs()

    def bfs(self, depth=0):
        response = ""
        for dir_ in self.contents["dirs"]:
            if depth > 0:
                response += ("|    " * depth)
            response += "| -- "
            response += f"{dir_.get_name()}\n"
            response += dir_.bfs(depth+1)
        for file_ in self.contents["files"]:
            if depth > 0:
                response += ("|    " * depth)
            response += "| -- "
            response += f"{file_.get_name()}\n"

        return response

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent

    def get_path(self):
        return f"{self.parent.get_path()}{self.name}/"

    def add_file(self, file_):
        self.contents["files"].append(file_)
        file_.set_parent(self)

    def add_dir(self, directory):
        self.contents["dirs"].append(directory)
        directory.set_parent(self)

    def get_contents(self):
        return self.contents["dirs"] + self.contents["files"]

    def get_files(self):
        return self.contents["files"]
    
    def get_dirs(self):
        return self.contents["dirs"]


class RootDir(Directory):
    def __init__(self):
        self.logger = Logger("game/directory/RootDir")
        
        super().__init__(None)

    def set_name(self, name: str):
        self.logger.log_alert("Root directory has no name.")
        return

    def set_parent(self, parent):
        self.logger.log_alert("Root directory has no parent directory.")
        return

    def get_path(self):
        return "/"
