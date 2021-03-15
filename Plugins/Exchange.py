import json
import Util
import os

from Portfolio import Portfolio
from Market import Market
from Config import Config
from Credentials import Credentials
from Plugin import Plugin

# Exchange Base Class
class Exchange(Plugin):
    def __init__(self, name, fromMap):
        super().__init__(name)
        #Util.Log(5, "Exchange.__init__(%s)" % name)
        self.Credentials = Credentials(self.Name())
        self.Cookies = {}
        toMap = {}
        for k,v in fromMap.items():
            toMap[v] = k # create the reverse mapping. We will need both to move data from and to the exchange from and to Trader
        self.Market = Market(fromMap, toMap) # tell our "market" class how to normalize from the exchanges data, to ours
        self.Portfolio = Portfolio()

    def Start(self):
        pass
    
    def Link(self, controller = None):
        pass
    
    def GetSystemStatus(self, args):
        raise Exception("You must implement GetSystemStatus() in your subclass")
    
    def BuyMarket(self, args):
        raise Exception("You must implement BuyMarket() in your subclass")

    def SellMarket(self, args):
        raise Exception("You must implement SellMarket() in your subclass")

    def GetAssets(self, args):
        raise Exception("You must implement GetAssets() in your subclass")

    def GetQuotes(self, args):
        return {"You must implement GetQuotes in your exchange:":self.Name}

if __name__ == "__main__":
    import sys
    #Collect().APIrequest('GET', sys.argv[1])
      	  

