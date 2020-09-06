import requests
from threading import Thread
import time


class ping(object):
    def __init__(self,id):
        self.url = "http://flusk.herokuapp.com/api/ping"
        self.id = id

    def ping(self):
        while True:
            resp = requests.post(self.url,{"id":self.id})
            if resp.status_code != 200:
                print("Error in ping function")
            time.sleep(70)
    def start(self):
        t = Thread(target=self.ping)
        t.start()
    
p = ping(2)
p.start()
while True:pass
a = 1