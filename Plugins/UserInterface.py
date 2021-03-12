import traceback
import json
import sys
import re
import Util
from TraderConfig import Config

class UserInterface:
    def __init__(self, name):
        self.Name = name
        self.Config = Config.GetConfig(self.Name)

    def Start(self, mod):
        self.Controller = mod
        
    def Response(self, package): # <== This is a callback! Don't use it directly, pass it in the Request
        try:
            print(Util.FormatContent(package))
        except Exception:
            data = sys.exc_info()
            Util.Log(1, traceback.print_tb(data[2]))

    def Request(self, command):
        try:
            self.Controller.DirectCall(command)
        except Exception:
            data = sys.exc_info()
            Util.Log(1, traceback.print_tb(data[2]))

    def do_assets(self, arg):
        raise Exception("You must define quote in your derived class")
        
    def do_quote(self, arg):
        raise Exception("You must define quote in your derived class")
            
    def do_monitor(self, arg):
        raise Exception("You must define monitor in your derived class")
            
    def do_exit(self, arg):
        raise Exception("You must define this in your derived class")
        
if __name__ == '__main__':
    import sys
    c = UI()
    c.cmdloop()
