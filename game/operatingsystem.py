import json

from utils.logger import Logger
from utils.ip_generator import IpGenerator
from utils.files_parser import FilesParser
from utils.exceptions import *
from game.directory import *
from game.terminal import *
from game.file import *


class OperatingSystem(object):
    def __init__(self, internet, username, password, rootdir):
        self.logger = Logger("game/operatinsystem/OperatingSystem")

        self.openterminals = []

        self.connected_to = []
        self.connected_from = []

        self.ip = IpGenerator.generate_ip()
        self.internet = internet
        self.username = username
        self.password = password
        self.rootdir = rootdir
        self.currentdir = self.rootdir
        self.mainterminal = self.open_terminal()
        self.logger.log_neutral(type(self.rootdir))

    def open_terminal(self, opened_by=None):
        terminal = Terminal(self, opened_by)
        self.openterminals.append(terminal)
        return terminal
    
    def close_temminal(self, terminal):
        self.openterminals.remove(terminal)


    def tree(self):
        return self.rootdir.tree()

    def get_obj_by_path(self, currentdir, path):
        destination = currentdir
        error = None
        if path == "":
            return self.rootdir
        path = path.split("/")
        if path[0] == "":
            path.pop(0)
            destination = self.rootdir
        if path[-1] == "": path.pop()
        
        for dirchange in path:
            if dirchange == "..":
                if not destination.get_parent():
                    error = "You are already in the root directory. You cannot go further outside."
                destination = destination.get_parent()
            elif dirchange == ".":
                continue
            else:
                try:
                    changed_dir = destination.get_obj_by_name(dirchange)
                except ObjNotFound:
                    error = f"Cannot find directory {'/'.join(path)}"
                else:
                    destination = changed_dir

        if error:
            raise PathNotFound(error)
        return destination


class BaseOS(OperatingSystem):
    def __init__(self, internet, username, password):
        self.logger = Logger("game/operatingsystem/BaseOS")
        with open("res/sample.json", "r") as f:
            rootdir = FilesParser.parse_root(json.load(f))
        super().__init__(internet, username, password, rootdir)
