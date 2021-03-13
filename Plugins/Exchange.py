import json
import Util
import os

from Portfolio import Portfolio
from Market import Market
from TraderConfig import Config
from Credentials import Credentials

# Exchange Base Class
class Exchange:
    def __init__(self, name, fromMap):
        self.Name(name)
        self.Config = Config.Branch(self.Name(), {})
        self.Credentials = Credentials.Get(self.Name())
        self.Cookies = {}
        toMap = {}
        for k,v in fromMap.items():
            toMap[v] = k # create the reverse mapping. We will need both to move data from and to the exchange from and to Trader
        self.Market = Market(fromMap, toMap) # tell our "market" class how to normalize from the exchanges data, to ours
        self.Portfolio = Portfolio()

    def Start(self, controller = None):
        # this may involve starting threads etc so its a separate step than init
        # this not always needed, especially if there is no passive feed coming from the exchange
        pass
        
    def GetConfig(self, key, default_value = None):
        return self.Config.Get(key, default_value)
        
    # the name of this exchange (used for sending commands and labelling output)
    def Name(self, name=None):
        if name:
            self.ExchangeName = name
        return self.ExchangeName
    
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
      	  

