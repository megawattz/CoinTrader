import traceback
import cmd2
import json
import sys
import re
import Util
from UserInterface import UserInterface

class TextUserInterface(cmd2.Cmd, UserInterface):
    def __init__(self, name = "TextUserInterface"):
        super().__init__(name)
        self.CommandLine = cmd2.Cmd()

    def Name(self):
        return self.Name

    # The controller loads all the modules of this app, and this module is one
    # of many possible UIs.  When the controller loads the module, it calls the
    # Start() function telling the UI to do it's thing. It also tells the UI
    # the function where commands should be sent "controllerEntryPoint"
    # Commands are a command name, followed by space delimited parameters

    def Start(self, mod):
        super().Start(mod)
        Util.Log(5, "Starting UIText")
        self.cmdloop()

    def do_load(self, args):
        elements = re.split('\s+', args)
        command = Util.ListToDict(elements, ["type", "filename"])
        Util.Log(5, command)
        self.Controller.Load(command)
        
     # ONLY USED IN Textual UIs
    def do_loglevel(self, arg):
        Util.LogLevel = arg
        self.Response("Format set to %s" % Util.LogLevel)

    def do_format(self, args):
        elements = re.split('\s+', args)
        command = Util.ListToDict(elements, ["format", "value"], {"command":"SetFormat", "value":0})
        self.Response(Util.SetFormat(command))

    def do_status(self, args):
        elements = re.split('\s+', args)
        command = Util.ListToDict(elements, ["target"], {"command":"GetSystemStatus", "target":'.'})
        self.Request(command)
        
    def do_assets(self, args):
        elements = re.split('\s+', args)
        command = Util.ListToDict(elements, ["target", "minimimum"], {"command":"GetPortfolio", "target":'.', "minimum": 0.0001})
        self.Request(command)
        
    def do_quote(self, args):
        elements = re.split('\s+', args)
        command = Util.ListToDict(elements, ["target"], {"command":"GetQuotes", "target":'.'}, "tickers")
        Util.Log(5, elements)
        self.Request(command)
            
    def do_monitor(self, args):
        elements = re.split('\s+', args)
        command = Util.ListToDict(elements, ["target"], {"command":"Monitor", "target":'.'}, "tickers")
        Util.Log(5, elements)
        self.Request(command)
        
    def do_exit(self, arg):
        self.Request("Detach", arg)
        
if __name__ == '__main__':
    import sys
    c = UI()
    #c.cmdloop()
    c.Start()
