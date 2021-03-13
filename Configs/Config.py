# config object
import os
import re
import sys
import Util
import json
from ConfigBase import ConfigBase

class Config(ConfigBase):

    def __init__(self, name = None):
        super().__init__()
        self.Root = self.Data[name];
        #Util.Log(5, "Config:%s\n" % name, json.dumps(self.Root, indent=2))
        
    def Get(self, key, default = None):
        levels = re.split("[.]+", key)
        branch = self.Root
        for level in levels:
            if not level in branch:
                if default != None:
                    return default
                else:
                    raise Util.TraderException("You must provide a config file: %s/%s.json for configuration key: %s" % (self.directory, level, key))
            branch = branch[level]
        return branch

   
