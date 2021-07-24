from game.file import File
from game.directory import Directory, RootDir
from utils.logger import Logger
from game.filesystem import FileSystem


class FilesParser(object):
    @staticmethod
    def parse_file_system(tree):
        rootdir = RootDir()

        dirs = tree["dirs"]
        files = tree["files"]
        
        for directory in dirs:
            rootdir.add_dir(FilesParser.parse_dir(directory))
        for file_ in files:
            rootdir.add_file(FilesParser.parse_file(file_))

        return FileSystem(rootdir)


    @staticmethod
    def parse_dir(directory):
        dir_to_return = Directory(directory["name"])

        subdirs = directory["dirs"]
        subfiles = directory["files"]
        
        for dir_ in subdirs:
            dir_to_return.add_dir(FilesParser.parse_dir(dir_))
        for file_ in subfiles:
            dir_to_return.add_file(FilesParser.parse_file(file_))

        return dir_to_return

    @staticmethod
    def parse_file(file_):
        return File(file_["name"], file_["ext"], file_["contents"])