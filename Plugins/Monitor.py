import json
import Util
import os

from TraderConfig import Config

# Monitor: a timed execution class that runs jobs and reports results
class Monitor:
    def __init__(self, name):
        self.Config = Config.Get(self.Name(), {})
        self.Credentials = Credentials.Get(self.Name())

    def Start(self, controller = None):
        pass
        
    def GetConfig(self, key, default_value = None):
        return self.Config.Get(key, default_value)
        
    # the name of this exchange (used for sending commands and labelling output)
    def Name(self, name=None):
        if name:
            self.Name = name
        return self.Name

    def Monitor(self, args):
        raise Exception("You must implement GetSystemStatus() in your subclass")

if __name__ == "__main__":
    import sys
    #Collect().APIrequest('GET', sys.argv[1])
      	  

