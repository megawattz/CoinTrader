import requests
import json
import os
import Utils

class API(object):
    # Generic Method to call APIs
    def Request(self, url, cookies={}, allow_redirects=True, **kwargs):
        response = requests.get(url, cookies=cookies, **kwargs)
        return response

if __name__ == "__main__":
    import sys
    #Collect().APIrequest('GET', sys.argv[1])
      	  

