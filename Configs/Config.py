# config object
import os
import re
import sys
import Util
import json
from ConfigBase import ConfigBase

class Config(ConfigBase):

    def __init__(self, name):
        self.Name(name)
        super().__init__()
        if not self.Name() in self.Data(): # no config file? (not always required)
            self.Data()[self.Name()] = {}
        self.Root = self.Data()[self.Name()];
        #Util.Log(5, "Config:%s\n" % name, json.dumps(self.Root, indent=2))

    def Name(self, name = None):
        if name:
            self.SectionName = name
        return self.SectionName
        
    def Get(self, key, default = None):
        levels = re.split("[.]+", key)
        branch = self.Root
        for level in levels:
            if not level in branch:
                if default != None:
                    return default
                else:
                    Util.Log(5, "CONFIG:", self.Root)
                    raise Util.TraderException("You must provide a config file: %s/%s.json for configuration key: %s" % (self.Directory(), self.Name(), key))
            branch = branch[level]
        return branch

   
