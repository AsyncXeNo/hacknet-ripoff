#!venv/bin/python3
import json

from utils.logger import Logger
from utils.files_parser import FilesParser
from game.directory import RootDir

logger = Logger("main")


def main():
    with open("res/sample.json", "r") as f:
        system = json.load(f)

    system = FilesParser.parse_file_system(system)
    logger.log(system.tree(), "neutral", True)
    logger.log_neutral("main")

if __name__ == "__main__":
    main()