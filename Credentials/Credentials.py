import json
import os
import re
import Util

class Credentials():

    # this is ALL the credentials
    Data = {}
    
    def __init__(self, name):
        self.Name = name
        if not self.Data:
            self.Load()
        # Root points to just the tree branch for the module using the credentials, "name" is the branch of the Data we want
        if not self.Name in self.Data:
            self.Data[self.Name] = {}
        self.Root = self.Data[self.Name]
        
    def Load(self):
        directory = os.path.dirname(__file__) # if directory not specified, use the same one as this Config.py file
        self.directory = directory # used later on in error messages is necessary
        fileNames = [fileName for fileName in os.listdir(directory) if re.search('.cred$', fileName)]
        if not fileNames:
            raise Util.TraderException("No config files in %s" % directory)
        for filename in fileNames:
            section = filename.removesuffix(".cred")
            try:
                self.Data[section] = Util.ReadJSONFile("%s/%s" % (directory, filename))
            except:
                Util.Log(2, filename, sys.exc_info())

    def Get(self,item_name, default = None):
        levels = re.split("[.]+",item_name)
        branch = self.Root
        for level in levels:
            if not level in branch:
                if default != None:
                    return default
                else:
                    raise Util.TraderException("You must provide a JSON config file: %s/%s.cred that defines a value for: \"%s\"" % (self.directory, self.Name, item_name))
            branch = branch[level]
        return branch

