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
        self.CacheFile = "Cache/"+self.Name()+".json"
        
    def Start(self):
        try:
            temp = Util.ReadFile(self.CacheFile)
            self.Data(json.loads(temp))
        except:
            Util.Log(5, "No cache file:", self.CacheFile)

    def Data(self, data_to_insert = None):
        # all the queries from remote sources are kept in one huge tree, but each plugin
        # stores it in that tree under the top level branch of whatever "dataroot" is configured for
        dataroot = self.Config.Get("dataroot", self.Name())
        if data_to_insert:
            self.Info[dataroot] = data_to_insert
        if not dataroot in self.Info:
            self.Info[dataroot] = {}
        return self.Info[dataroot]
    
    def RefreshThread(self):
        self.Controller.PluginResponse(self.Name(), "Refresh Started")
        config = self.Config.Get()
        Util.Log(5, "Request:", json.dumps(config))
        temp = self.Request(url=config['url'], headers=config['headers'])
        Util.Log(5, "HttpDataQuery Refresh:", temp.text)
        data = json.loads(temp.text)
        Util.WriteFile(self.CacheFile, json.dumps(data, indent=2), backup=True)
        self.Data(data)
        self.Controller.PluginResponse(self.Name(), "Refresh Finished")
    
    def Refresh(self, args = None):
        Util.Log(5, "Refresh:", args)
        self.Thread = threading.Thread(target=self.RefreshThread)
        self.Thread.start()
    
    # does the JSON query match the JSON data?
    def Hit(self, label, data, query, collector):
        if not query:
            collector[label] = data
            return
        search = query.pop(0)
        #Util.Log(5, "Hit label:%s search:%s %s:%s" % (label, search, label, data))
        if isinstance(data, list):
            for index in range(0, len(data)):
                self.Hit(index, data[index], query, collector)
        else:
            if isinstance(data, dict):
                for key, value in data.items():
                    if re.match(search, key):
                        self.Hit(key, value, query, collector)
            else:
                collector[label] = data
    
    def Query(self, args):
        Util.Log(5, "Query:", args)
        elements = re.split(':', args['query'])
        collector = {}
        if args['target'] == '*':
            self.Hit(self.Name(), self.Info, elements, collector)
        else:
            self.Hit(self.Name(), self.Data(), elements, collector)
        return collector

if __name__ == "__main__":
    database = Database()
    data = database.Start()
    print(json.dumps(data.Query(""), indent=4))
    
