# config object
import os
import re
import sys
import Util
import json

class Config():
    def __init__(self, directory = None):
        self.Load(directory)
        
    def Load(self, directory = None):
        if not directory:
            directory = os.path.dirname(__file__) # if directory not specified, use the same one as this Config.py file
        self.directory = directory
        self.Config = {}
        fileNames = [fileName for fileName in os.listdir(directory) if re.search('.json$', fileName)]
        if not fileNames:
            raise Util.TraderException("No config files in %s" % directory)
        for filename in fileNames:
            section = filename.removesuffix(".json")
            try:
                self.Config[section] = Util.ReadJSONFile("%s/%s" % (directory, filename))
            except:
                Util.Log(2, filename, sys.exc_info())
        #Util.Log(5, "Config:", json.dumps(self.Config, indent=2))
                
    def Get(self, key, default = None):
        levels = re.split("[.]+", key)
        branch = self.Config
        for level in levels:
            if not level in branch:
                if default != None:
                    return default
                else:
                    raise Util.TraderException("You must provide a config file: %s/%s.json for configuration key: %s" % (self.directory, level, key))
            branch = branch[level]
        return branch
    
    def __getitem__(self, key):
        return self.GetConfig(key)

   
