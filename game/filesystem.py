from utils.logger import Logger
from game.directory import *
from game.terminal import *
from game.file import *


class FileSystem(object):
    def __init__(self, rootdir):
        self.rootdir = rootdir
        self.currentdir = rootdir
        self.terminal = Terminal(self)

    def tree(self):
        return self.rootdir.tree()
