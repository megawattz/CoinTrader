import json
import sys
import traceback
import re
import Util
from Database import Database
from API import API

class HttpDataFeed(Database, API):
    def __init__(self, name):
        Database.__init__(self, name)
        
    def Start(self):
        self.Data(self.Request(self.Config.Get("url")))
        pass

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
    
