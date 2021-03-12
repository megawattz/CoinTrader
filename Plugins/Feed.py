# base class for a continuous feed of information from an exchange

class Feed():
    ManagerHandle = None
    
    Streams = {
        "Account": None,
        "Trade": None,
        "Price": None,
    }

    def __init__(self, managerHandle):
        self.ManagerHandle = managerHandle;

    def AddStream(self, id, description, callback):
        Streams[id] = { description, callback }
        
        
