# base class defining current market data
import Util
import re

class Market:
    def __init__(self, fromMap, toMap):
        self.FromMap = fromMap
        self.ToMap = toMap
        self.Commodities = {} #IMPORTANT: Data is saved in the FOREIGN FORMAT because its huge, and we dont' want to convert it to local mappings until we actually use it

    def Set(self, ticker, commodities):
        self.Commodities = commodities

    def SetCommodity(self, ticker, data):
        self.Commodities[ticker] = data
        
    def GetCommodity(self, ticker):
        if ticker not in self.Commodities:
            return None
        foreign = self.Commodities[ticker]
        translated = {}  # normalize data for usage 
        for key in self.FromMap: # iteraate through the properties we are interested in for this Commodity data
            if key in foreign:
                ourkey = self.FromMap[key] # get our name for it
                translated[ourkey] = foreign[key];  # "ticker" is the symbol of the commodity
        return translated
        
    def Get(self, ticker_wildcards):
        commodities = {}
        for ticker_wildcard in ticker_wildcards:
            for ticker in self.Commodities:
                if re.match(ticker_wildcard, ticker):
                    item = self.GetCommodity(ticker)
                    if item:
                        commodities[ticker] = item
        return commodities

