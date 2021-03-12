import requests
import json
import os
import Utils

class API(object):
    # Generic Method to call APIs
    def APIrequest(self, url, cookies={}, allow_redirects=True, **kwargs):
        cookies = cookies or self.Cookies
        response = requests.get(url, cookies=cookies, **kwargs)
        self.Cookies = response.getCookies();
        return response

if __name__ == "__main__":
    import sys
    #Collect().APIrequest('GET', sys.argv[1])
      	  

