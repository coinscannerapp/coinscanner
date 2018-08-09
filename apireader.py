import requests
import datetime
import threading
import json
# import urllib.request

url = "https://api.binance.com/api/v1/trades?symbol={}&limit={}"
coinpair = "BTCUSDT"
limit = 1
class PricePoint(object):
    def __init__(self, **kwargs):
        self._time = kwargs["time"]
        self._price = kwargs["price"]
        self._name = kwargs["name"]
    def time(self, time=None):
        if time: self._time = time

        return self._time
    def price(self, price=None):
        if price: self._price = price
        return self._price
    def time(self, name=None):
        if name: self._name = name
        return self._name
    def __str__(self):
        return f'{self._name} costs {self._price} at {self._time}'

print('-'*40)
def fromBinance():
    response = requests.get(url.format(coinpair,limit))
    # print(url.format(coinpair,limit))
    content = response.json()
    print(content)
    priceFromApi = content[0]
    time = datetime.datetime.fromtimestamp(priceFromApi["time"]/1000.0)
    pricepoint = PricePoint(name="BTCUSDT", price=priceFromApi["price"], time=time)
    # decoded = json.loads(content)
    # alternative solution
    # jsonurl = urllib.request.urlopen(url.format(coinpair, limit))
    # content = json.loads(jsonurl.read()) # <-- read from it
    
    # data = json.loads(content.read())
    # print(type(content))
    # for key, value in content[0].items():
    #     print(key)
    print(pricepoint)
# printFromBinance()

ms = 1530881734550
time = datetime.datetime.fromtimestamp(ms/1000.0)
print(time)
print('-'*40)

# data = {"id":55311918,"price":"6551.01000000","qty":"0.01912400","time":1530888563135,"


class TaskThread(threading.Thread): # inherits from threading.Thread class
    """Thread that executes a task every N seconds"""
    
    def __init__(self):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 15.0
    
    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval
    
    def shutdown(self):
        """Stop this thread"""
        self._finished.set()
    
    def run(self):
        while 1:
            if self._finished.isSet(): return
            self.task()
            
            # sleep for interval or until shutdown
            self._finished.wait(self._interval)
    
    def task(self):
        """The task done by this thread - override in subclasses"""
        print('errrrrrrrrrrrrrrorororrorororoor')

class Datareader(TaskThread):
    def __init__(self, task):
        super().__init__()
        self.task = task
    

datareader = Datareader(task=fromBinance)
datareader.setInterval(1.0)
datareader.run()

