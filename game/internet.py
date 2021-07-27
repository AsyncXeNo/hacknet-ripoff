from utils.logger import Logger
from utils.exceptions import *
from game.operatingsystem import BaseOS


class Internet(object):
    def __init__(self, systems={}):
        self.logger = Logger("game/internet/Internet")
        self.systems = systems

    def addOS(self, os_id, username, password):
        self.systems[os_id] = BaseOS(self, username, password)

    def get_os_by_ip(self, ip):
        for os in self.systems:
            if self.systems[os].ip == ip:
                return self.systems[os]
        raise OsNotFound(f"No system with ip {ip}")