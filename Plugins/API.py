import requests
import json
import os
import Util

class API(object):
    # Generic Method to call APIs
    def Request(self, url, cookies={}, allow_redirects=True, **kwargs):
        Util.Log(5, "Request:", url)
        response = requests.get(url, cookies=cookies, **kwargs)
        Util.Log(5, "Response:", response)
        return response

if __name__ == "__main__":
    import sys
    #Collect().APIrequest('GET', sys.argv[1])
      	  

