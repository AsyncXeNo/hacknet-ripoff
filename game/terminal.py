import shlex

from utils.exceptions import FileNotFound, PathNotFound
from utils.logger import Logger
from game.file import *
from game.directory import *


class Terminal(object):
    def __init__(self, os, opened_by):
        self.logger = Logger("game/teminal/Terminal")

        self.os = os
        self.opened_by = opened_by
        self.connected_to = None
        self.currentdir = self.os.currentdir
        
        self.cmd_in_progress = False
        self.subcommand = None
        self.special_commands = {
            "connect": self.connect,
            "disconnect": self.disconnect
        }
        self.commands = {
            "cd": self.cd,
            "tree": self.tree,
            "ls": self.ls,
            "touch": self.touch,
            "write": self.write,
            "cat": self.cat,
            "replace": self.replace,
            "ip": self.ip,
            "connect": self.connect,
            "disconnect": self.disconnect,
            "dc": self.disconnect,
            "echo": self.echo,
            "rm": self.rm,
        }


    def run(self, args):
        if self.connected_to:
            self.logger.log_neutral("remotely executing command.")
            return self.connected_to.run(args)
        if len(args) == 0:
            return self.new_line()
        if not self.cmd_in_progress:
            cmd = args.pop(0)
            try:
                return self.commands[cmd](args)
            except KeyError:
                return self.response(1, None, f"{cmd} command not found.")
                
        elif self.subcommand:
            return self.subcommand(args)
        
    def echo(self, args):
        output = " ".join(args)
        return self.response(0, output, None)    

    def connect(self, args):
        if self.opened_by != None:
            return self.response(1, None, "You need to disconnect from the current system in order to connect to a new one.")
        if len(args) < 1:
            return self.response(1, None, "You did not provide an ip to connect to.")
        
        ip = args[0]
        system = self.os.internet.get_os_by_ip(ip)
        terminal = system.open_terminal(self)
        self.connected_to = terminal
        return self.response(0, f"Connected to {system.ip}", None)

    def disconnect(self, _):
        if self.opened_by == None:
            return self.response(1, None, "You are not connected to any system.")
        ip = self.os.ip
        self.opened_by.connected_to = None
        self.opened_by = None
        return self.response(0, f"Disconnected from {ip}", None)

    def ip(self, _):
        return self.response(0, self.os.ip, None)
    
    def replace(self, args):
        if len(args) < 1:
            return self.response(1, None, "Syntax: replace sample.txt \"Hello\" \"Bye\"")
            
            return
        elif len(args) < 2:
            return self.response(1, None, "Syntax: replace sample.txt \"Hello\" \"Bye\"")
            
            return

        path = args.pop(0)
        if len(path.split("/")) > 1:
            destinationdir = "/".join(path.split("/")[:-1])
        else:
            destinationdir = self.currentdir.get_path()
        try:
            destinationdir = self.os.get_obj_by_path(self.currentdir, destinationdir)
        except ObjNotFound:
            return self.response(1, None, "Directory not found.")
            
            return
        if not (type(destinationdir) in [Directory, RootDir]):
            return self.response(1, None, "Directory not found.")
            
            return

        filename = path.split("/").pop()
        try:
            file_to_write = destinationdir.get_file_by_name(filename)
        except FileNotFound:
            return self.response(1, None, f"File with name {filename} does not exist.")
            return

        args = " ".join(args)
        try:
            args = shlex.split(args)
        except:
            self.replace(1, None, "Invalid syntax.\nSyntax: replace sample.txt \"Hello\" \"Bye\"")
            return
        if len(args) > 2:
            return self.response(1, None, "Invalid syntax.\nSyntax: replace sample.txt \"Hello\" \"Bye\"")
            return

        file_to_write.replace(args[0], args[1])
        return self.response(0, None, None)

    def write(self, args):
        if len(args) < 1:
            return self.response(1, None, "You need to write the file path that you wish to write to.\nSyntax: write sample.txt \"Hello World!\"")
            
            return
        elif len(args) < 2:
            return self.response(1, None, "You need to write the content in quotes.\nSyntax: write sample.txt \"Hello World!\"")
            
            return

        path = args.pop(0)
        if len(path.split("/")) > 1:
            destinationdir = "/".join(path.split("/")[:-1])
        else:
            destinationdir = self.currentdir.get_path()

        try:
            destinationdir = self.os.get_obj_by_path(self.currentdir, destinationdir)
        except ObjNotFound:
            return self.response(1, None, "Directory not found.")
            
            return
        if not (type(destinationdir) in [Directory, RootDir]):
            return self.response(1, None, "Directory not found.")
            
            return

        filename = path.split("/").pop()

        try:
            file_to_write = destinationdir.get_file_by_name(filename)
        except FileNotFound:
            return self.response(1, None, f"File with name {filename} does not exist.")
            
            return

        content = " ".join(args)
        if not (content.startswith('"') and content.endswith('"')):
            return self.response(1, None, "You need to write the content in quotes.\nSyntax: write sample.txt \"Hello World!\"")
            
            return
        
        content = content[1:-1]
        file_to_write.write(content)
        return self.response(0, None, None)


    def cat(self, args):
        if len(args) < 1:
            return self.response(1, None, "You need to provide a file name.\nSyntax: cat sample.txt")
            
            return

        path = args.pop(0)
        if len(path.split("/")) > 1:
            destinationdir = "/".join(path.split("/")[:-1])
        else:
            destinationdir = self.currentdir.get_path()

        try:
            destinationdir = self.os.get_obj_by_path(self.currentdir, destinationdir)
        except ObjNotFound:
            return self.response(1, None, "Directory not found.")
            
            return
        if not (type(destinationdir) in [Directory, RootDir]):
            return self.response(1, None, "Directory not found.")
            
            return

        filename = path.split("/").pop()

        try:
            file_to_read = destinationdir.get_file_by_name(filename)
        except FileNotFound:
            return self.response(1, None, f"File with name {filename} does not exist.")
            
        return self.response(0, file_to_read.read(), None)


    def rm(self, args):
        path = "" if len(args) < 1 else args[0]
        if path == "":
            return self.response(1, None, "You did not provide a file name.")

        obj = self.os.get_obj_by_path(path)
        obj.get_parent().delete(obj)
        return self.response(0, None, None)

    def touch(self, args):
        path = "" if len(args) < 1 else args[0]
        if len(path.split("/")) > 1:
            destinationdir = "/".join(path.split("/")[:-1])
        else:
            destinationdir = self.currentdir.get_path()

        try:
            destinationdir = self.os.get_obj_by_path(self.currentdir, destinationdir)
        except ObjNotFound:
            return self.response(1, None, "Directory not found.")
            
        if not (type(destinationdir) in [Directory, RootDir]):
            return self.response(1, None, "Directory not found.")
            

        if path == "":
            return self.response(1, None, "You did not provide a file name.")
            

        filename = path.split("/").pop().split(".")
        if len(filename) == 1:
            name = filename[0]
            ext = None
        elif len(filename) == 2:
            name = filename[0]
            ext = filename[-1]
        else:
            name = filename[0:-1]
            ext = filename[-1]
        newfile = File(name, ext)
        destinationdir.add_file(newfile)
        return self.response(0, None, None)


    def cd(self, args):
        path = "" if len(args) < 1 else args[0]

        try:
            destinationdir = self.os.get_obj_by_path(self.currentdir, path)
        except PathNotFound:
            return self.response(1, None, "Path not found.")
            
            return
        if not (type(destinationdir) in [Directory, RootDir]):
            return self.response(1, None, "Path is not a directory.")
            
            return

        self.currentdir = destinationdir
        self.logger.log_neutral(f"Changed into dir {self.currentdir.get_path()}")
        return self.response(0, None, None)
        


    def ls(self, _):
        contents = [content.get_name() for content in self.currentdir.get_contents()]
        stdout = "\n".join(contents)
        self.logger.log(stdout, "neutral", True)
        return self.response(0, stdout, None)


    def tree(self, _):
        self.logger.log(self.currentdir.tree(), "neutral", True)
        return self.response(0, self.currentdir.tree(), None)
        
    def subcommand(self, function, output):
        self.subcommand = function
        return output

    def response(self, code, stdout, stderr):
        if stdout and stderr:
            return f"Command exited with code {code}" + f"\n{stdout}" + f"\n{stderr}"
        elif stderr:
            self.logger.log_error(stderr)
            return f"Command exited with code {code}" + f"\n{stderr}"
        elif stdout:
            return f"Command exited with code {code}" + f"\n{stdout}"
        else:
            return f"Command exited with code {code}"


    def new_line(self):
        if self.connected_to:
            return self.connected_to.new_line()
        self.subcommand = None
        self.cmd_in_progress = False
        name = self.os.username if not self.opened_by else f"{self.opened_by.os.ip}(guest)" 
        return f"{name}:{self.currentdir.get_path()}$ "
