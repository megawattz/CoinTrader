import traceback
import json
import sys
import re
import Util
from Config import Config
from Plugin import Plugin

class UserInterface(Plugin):
    def __init__(self, name):
        super().__init__(name)
        Util.Log(5, "UserInterface:", name)

    def Start(self):
        pass

    def Link(self, controller):
        # The controller loaded this module, so this module needs to be
        # informed how to call the controller
        self.Controller = controller
        #Util.Log(5, "Controller Link: ", self.Controller)

    def Response(self, response_json): # <== This is a callback! Don't use it directly, the Controller will send responses here
        try:
            print(Util.FormatContent(response_json))
        except Exception:
            data = sys.exc_info()
            Util.Log(2, traceback.print_tb(data[2]))

    def Request(self, command):
        try:
            self.Controller.PluginRequest(command)
        except Exception:
            data = sys.exc_info()
            Util.Log(2, data)
            Util.Log(2, traceback.print_tb(data[2]))

    def do_assets(self, arg):
        raise Exception("You must define quote in your derived class")

    def do_quote(self, arg):
        raise Exception("You must define quote in your derived class")

    def do_monitor(self, arg):
        raise Exception("You must define monitor in your derived class")

    def do_query(self, arg):
        raise Exception("You must define this in your derived class")

    def do_list(self, arg):
        raise Exception("You must define this in your derived class")

    def do_exit(self, arg):
        raise Exception("You must define this in your derived class")

if __name__ == '__main__':
    import sys
    c = UI()
    c.cmdloop()
