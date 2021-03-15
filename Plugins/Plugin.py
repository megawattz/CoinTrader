import Util
from Config import Config

class Plugin:
    def __init__(self, name):
        self.Name(name)
        Util.Log("Load:", self.Name())
        self.Config = Config(self.Name())
        
    def Name(self, name = None):
        if name:
            self.PluginName = name
        return self.PluginName
    
