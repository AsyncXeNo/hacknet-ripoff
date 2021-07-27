#!venv/bin/python3
import time
import json
import pickle

from utils.logger import Logger
from utils.id_generator import IdGenerator
from game.operatingsystem import BaseOS
from game.internet import Internet

logger = Logger("main")


def main():
    with open("data/internet.pickle", "rb") as f:
        internet = pickle.load(f)
    outputs = {}
    
    while True:
        time.sleep(1)
        try:
            with open("data/input.json", "r+") as f:
                inputs = json.load(f)
                f.truncate(0)
                f.seek(0)
                json.dump([], f, indent=4)

            for entry in inputs:
                if not "id" in entry.keys():
                    newid = IdGenerator.generate_id()
                    internet.addOS(newid, entry["username"], entry["password"])
                    outputs[entry["tempid"]] = newid
                    with open("data/internet.pickle", "wb") as f:
                        pickle.dump(internet, f)
                else:
                    mainterminal = internet.systems[entry["id"]].mainterminal
                    outputs[entry["id"]] = (mainterminal.run(entry["cmd"].strip().split(" ")), mainterminal.new_line())
            
            with open("data/output.json", "w") as f:
                json.dump(outputs, f, indent=4)
                
        except IOError:
            continue
        except KeyError as e:
            logger.log_neutral(e)
            continue
        

if __name__ == "__main__":
    main()