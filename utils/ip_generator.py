import string
import random
import json

from utils.logger import Logger


class IpGenerator(object):
    @staticmethod
    def generate_ip(length:int=8):
        with open("data/generated_ips.json", "r") as f:
            generated = json.load(f)

        ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

        while ip in generated:
            ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

        generated.append(ip)
        
        with open("data/generated_ids.json", "w") as f:
            json.dump(generated, f, indent=4)
            
        return ip