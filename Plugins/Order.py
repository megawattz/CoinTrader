# base class for an order on a market

class Order:
    def __init__(self, ticker, ordertype, code = None):
        self.Ticker = ticker
        self.OrderType = ordertype
        self.Code = code # this would be python code on what the order is supposed to do.
    
