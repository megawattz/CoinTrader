# config object
import os
import re
import sys
import Util
import json

class ConfigBase():
    
    ConfigData = {}
    
    def __init__(self, directory = os.path.dirname(__file__)):
        self.Directory(directory)
        if self.ConfigData: # already read in all the configs?
            return
        if not directory:
            directory = os.path.dirname(__file__) # if directory not specified, use the same one as this Config.py file
            Util.Log(5, "Loading Configs from: ", directory)
        fileNames = [fileName for fileName in os.listdir(self.Directory()) if re.search('.json$', fileName)]
        if not fileNames:
            raise Util.TraderException("No config files in %s" % self.Directory())
        for filename in fileNames:
            section = filename.removesuffix(".json")
            try:
                self.ConfigData[section] = Util.ReadJSONFile("%s/%s" % (self.Directory(), filename))
                Util.Log(5, "Loaded Config file:%s into Config section:%s" % (filename, section))
            except:
                Util.Log(2, filename, sys.exc_info())

    def Data(self):
        return self.ConfigData
    
    def Directory(self, directory = None):
        if directory:
            self.ConfigDir = directory
        return self.ConfigDir
    
            
