import json
import sys
import traceback
import Util
from Exchange import Exchange

from binance.client import Client as BinanceClient
from binance.websockets import BinanceSocketManager

class Binance(Exchange):

    PropertyMap = { 
        's':'ticker',
        'c':'price',
        'v':'volumeUSD',
        'b':'bid',
        'a':'ask'
    }
        
    def __init__(self, name="Binance", **kwargs):
        super().__init__(name, self.PropertyMap)

    # all these Callback functions handle the incoming, continual streams from Binance. 
    def AssetsCallback(self, message):
        print(Util.FormatContent(message))
      
    def TradeCallback(self, message):
        print(Util.FormatContent(message))
        
    # store the incoming coin data from the exchange
    def CommoditiesCallback(self, msg):
        # example of a binance feed msg  
        #{'e': '24hrTicker', 'E': 1614481299899, 's': 'REEFBUSD', 'p': '-0.00080000', 'P': '-2.596', 'w': '0.03145464', 'x': '0.03082000', 'c': '0.03002000', 'Q': '1911.20000000', 'b': '0.03001000', 'B': '913.70000000', 'a': '0.03004000', 'A': '13727.20000000', 'o': '0.03082000', 'h': '0.03400000', 'l': '0.02993000', 'v': '57182684.00000000', 'q': '1798660.45869900', 'O': 1614394893867, 'C': 1614481293867, 'F': 86942, 'L': 104149, 'n': 17208},
        # since this is a continuous feed handler, we want to minimize processing, so for this type of data we don't try to normalize it.
        # We normalize it when we pull it out of the "Market" Object, since querying occurs alot fewer times than the continual 24x7 feeding coming in.
        for commodity in msg:
            ticker = commodity['s']
            self.Market.SetCommodity(ticker, commodity)

    def Start(self, controller = None):
        self.Client = BinanceClient(self.Credentials['key'], self.Credentials['secret'])
        self.Feeds(True)
        
    def Feeds(self, on = True):
        if on == True:
            self.Feed = BinanceSocketManager(self.Client, user_timeout = 20) #self.Config.Get("feed_timeout", 20))
            self.Feed.start_user_socket(self.AssetsCallback)
            self.Feed.start_ticker_socket(self.CommoditiesCallback) #, int(self.Config.Get("ticker_update", 5)))
            self.Feed.start()
            Util.Log(6, "Connected")
        if on == False:
            try:
                self.Feed.close()
                print("Binance Closing Feeds")
            except:
                pass
                #self.Feed = Feed(feedManager)

    def GetSystemStatus(self, args):
        return self.Client.get_system_status()
                
    def GetPortfolio(self, args):
        minimum = 0
        if not 'minimum' in args:
            minimum = Config.Get("portfolio.minimum", 0.0001) # Gets a config value, but also requires a default in case config has not been set
        minimim_balance = float(miniumm)
        data = self.Client.get_account()
        balances = data['balances']
        for item in balances:
            if float(item['free']) >= minimum_balance or float(item['locked']) >= minimum_balance:
                ticker = item['asset']
                self.Portfolio.SetAsset(ticker, item['free'], item['locked'])
        return self.Portfolio.Get()
    
    def GetQuotes(self, args):
        Util.Log(5, args)
        return self.Market.Get(args['tickers'])
    
    def __del__(self):
        self.Feeds(False)

if __name__ == "__main__":
    exchange = Exchange()
    data = exchange.GetPortfolio({'minimum':1.0})
    print(json.dumps(data, indent=4))
    #data = sys.exc_info()
    #print(exchange.Name(), data[1])

        
