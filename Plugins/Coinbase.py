import json
from Exchange import Exchange
import cbpro

class Coinbase(Exchange):
    PropertyMap = {
    }
    
    def __init__(self, name="Coinbase", **kwargs):
        super().__init__(name, self.PropertyMap)

    #def Update(self):
        #self.FeedManager = cbporo.WebsocketCient(url="wss://ws-feed.pro.coinbase.com")

    def Start(self, controller = None):
        self.Client = cbpro.AuthenticatedClient(self.Credentials['key'],
                                                self.Credentials['secret'],
                                                self.Credentials['password']
                                                )
    def GetPortfolio(self, args):
        balances = self.Client.get_accounts()
        minimum_balance = float(args['minimum'] or 0.0001)
        self.Portfolio.Set({})
        for item in balances:
            if float(item['available']) >= minimum_balance or float(item['hold']) >= minimum_balance:
                ticker = item['currency']
                self.Portfolio.SetAsset(ticker, item['available'], item['hold'])
        return self.Portfolio.Readable()

if __name__ == "__main__":
    exchange = Exchange()
    data = exchange.GetAssets()
    print(json.dumps(data, indent=4))
        
