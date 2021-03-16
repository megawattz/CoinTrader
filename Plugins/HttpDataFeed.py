import json
import sys
import traceback
import re
import Util
import threading
from Database import Database
from API import API

class HttpDataFeed(Database, API):
    Info = {} # all data feeds will share a large shared JSON tree so joins can be done easily
    
    def __init__(self, name):
        Database.__init__(self, name)
        
    def Start(self):
        pass

    def Data(self, json_branch = None):
        if json_branch:
            self.Info[self.Name()] = json_branch
        if not self.Name() in self.Info:
            self.Info[self.Name()] = {}
        return self.Info[self.Name()]
    
    def RefreshThread(self):
        self.Controller.PluginResponse(self.Name(), "Refresh Started")
        config = self.Config.Get()
        Util.Log(5, "Request:", json.dumps(config))
        temp = self.Request(url=config['url'], headers=config['headers'])
        Util.Log(5, "HttpDataQuery Refresh:", temp)
        self.Data(temp.text)
        self.Controller.PluginResponse(self.Name(), "Refresh Finished")
    
    def Refresh(self, target = None):
        Util.Log(5, "Refresh:", target)
        self.Thread = threading.Thread(target=self.RefreshThread)
        self.Thread.start()
    
    # does the JSON query match the JSON data?
    def Hit(self, data, query):
        for key in query:
            if not data[key]: # data doesn't even have that key? no hit
                return None
            selector = query[key]
            if not re.match(selector, data[key]):
                return None
        return data # A hit, return it.
    
    def Query(self, query, options = {}):
        return self.Data()
        results = []
        for item in self.Data():
            data = self.Data()[item]
            if self.Hit(data, query):
                results.append[data]
        return results

if __name__ == "__main__":
    database = Database()
    data = database.Start()
    print(json.dumps(data.Query(""), indent=4))
    
