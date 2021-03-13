# config object
import os
import re
import sys
import Util
import json

class ConfigBase():
    
    Data = {}
    
    def __init__(self, directory = None):
        if self.Data:
            return
        if not directory:
            directory = os.path.dirname(__file__) # if directory not specified, use the same one as this Config.py file
            Util.Log(5, "Loading Configs from: ", directory)
        self.directory = directory
        fileNames = [fileName for fileName in os.listdir(directory) if re.search('.json$', fileName)]
        if not fileNames:
            raise Util.TraderException("No config files in %s" % directory)
        for filename in fileNames:
            section = filename.removesuffix(".json")
            try:
                self.Data[section] = Util.ReadJSONFile("%s/%s" % (directory, filename))
            except:
                Util.Log(2, filename, sys.exc_info())

   
