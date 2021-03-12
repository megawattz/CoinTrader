# base class to define a portfolio on an exchange

class Asset():
    def __init__(self, ticker, initialFree = 0, encumbered = 0):
        self.Set(ticker, float(initialFree), float(encumbered))

    def Set(self, ticker, free, encumbered = 0):
        self.Properties = {'ticker':ticker, 'available':float(free), 'encumbered':float(encumbered)}
        return self
    
    def Get(self):
        return self.Properties

class Portfolio():
    def __init__(self, assets = {}):
        self.Assets = assets

    def Set(self, assets = {}):
        self.Assets = assets
        return self.Assets

    def Get(self):
        return self.Assets

    def GetAsset(self, ticker):
        return self.Assets[ticker].Get()
    
    def SetAsset(self, ticker, free, encumbered):
        self.Assets[ticker] = Asset(ticker, free, encumbered)
        return self

    def Readable(self):
        readable = {}
        for ticker in self.Assets:
            readable[ticker] = self.Assets[ticker].Get()
        return readable
    
       
