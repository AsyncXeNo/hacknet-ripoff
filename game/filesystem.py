from utils.logger import Logger
from game.directory import *
from game.file import *


class FileSystem(object):
    def __init__(self, rootdir):
        self.rootdir = rootdir
        self.currentdir = rootdir

    def tree(self):
        return self.rootdir.tree()
