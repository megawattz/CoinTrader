import json
import os

class Credentials():

    def __init__(self, name):
        self.Load()
        if not name in self.Data:
            self.Root[name] = {}
        self.Root = self.Data[name]
        
    def Load(self, directory = None):
        if not directory:
            directory = os.path.dirname(__file__) # if directory not specified, use the same one as this Config.py file
        self.directory = directory
        self.Data = {}
        fileNames = [fileName for fileName in os.listdir(directory) if re.search('.cred$', fileName)]
        if not fileNames:
            raise Util.TraderException("No config files in %s" % directory)
        for filename in fileNames:
            section = filename.removesuffix(".json")
            try:
                self.Data[section] = Util.ReadJSONFile("%s/%s" % (directory, filename))
            except:
                Util.Log(2, filename, sys.exc_info())

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

