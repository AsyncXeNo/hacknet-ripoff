from utils.logger import Logger


class Terminal(object):
    def __init__(self, filesystem):
        self.logger = Logger("game/teminal/Terminal")

        self.filesystem = filesystem

    def run(self, cmd):
        pass
