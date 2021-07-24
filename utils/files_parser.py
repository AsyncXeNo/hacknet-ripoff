from game.file import File
from game.directory import Directory, RootDir
from utils.logger import Logger
from game.filesystem import FileSystem


class FilesParser(object):
    logger = Logger("utils/files_parser/FilesParser")

    @staticmethod
    def parse_file_system(data):
        rootdir = RootDir()

        dirs = []
        files = []

        for content in data:
            if type(content["contents"]) == list:
                dirs.append(content)
            else:
                files.append(content)
        
        for directory in dirs:
            rootdir.add_dir(FilesParser.parse_dir(directory))
        for file_ in files:
            rootdir.add_file(FilesParser.parse_file(file_))

        return FileSystem(rootdir)


    @staticmethod
    def parse_dir(directory):
        dir_to_return = Directory(directory["name"])

        subdirs = []
        subfiles = []

        for content in directory["contents"]:
            if type(content["contents"]) == list:
                subdirs.append(content)
            else:
                subfiles.append(content)
        
        for dir_ in subdirs:
            dir_to_return.add_dir(FilesParser.parse_dir(dir_))
        for file_ in subfiles:
            dir_to_return.add_file(FilesParser.parse_file(file_))

        return dir_to_return

    @staticmethod
    def parse_file(file_):
        fullname = file_["name"].split(".")
        if len(fullname) < 1:
            FilesParser.logger.log_error("Cannot create file with no name.")
            raise Exception("Cannot create file with no name.")
        elif len(fullname) == 1:
            name = fullname[0]
            ext = None
        elif len(fullname) == 2:
            name = fullname[0]
            ext = fullname[-1]
        else:
            name = ".".join(fullname[:-1])
            ext = fullname[-1]
        return File(name, ext, file_["contents"])