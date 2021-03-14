import json
import os
import Util
from Config import Config
from Credentials import Credentials
from Plugin import Plugin

# Exchange Base Class
class Database(Plugin):
    def __init__(self, name):
        super().__init__(name)
        self.Credentials = Credentials(self.Name())
        self.Info = {};

    def Data(self, data):
        if data:
            self.Info = data
        return self.Info
    
    def Link(self, controller = None):
        pass
    
    def Start(self):
        # this may involve starting threads etc so its a separate step than init
        # this not always needed, especially if there is no passive feed coming from the exchange
        pass

    def Fetch(self):
        raise TraderException("Your plugin must implement this")

    def Refresh(self):
        raise TraderException("Your plugin must implement this")
    
    def Query(self, query):
        raise TraderException("Your plugin must implement this")

if __name__ == "__main__":
    import sys
    #Collect().APIrequest('GET', sys.argv[1])
      	  

