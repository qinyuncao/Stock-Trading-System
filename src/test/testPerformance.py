import time
import requests
import random
from threading import Thread

class Client:
    def __init__(self, p, stocks, url, frontAddr):
        self.session = requests.session()
        self.p = p
        self.stockName = stocks
        self.url = url
        self.frontAddr = frontAddr

    def run(self):
        while 1:
            message = input('Latency for Lookup(1) or Trade(2):')
            if str(message) == '1':
                self.lookupLatency()
            elif str(message) == '2':
                self.tradeLatency()
            else:
                print("Wrong Code!!!")
    # Test latency for lookup
    def lookupLatency(self):
        start_time = time.time()
        for i in range(100):
            r = self.session.get(url=self.url + self.stockName[random.randint(0, 3)]).json()
        end_time = time.time()
        avg_time = (end_time - start_time) / 100
        print("average running time for look up is " + str(avg_time))


    # Test latency for trade
    def tradeLatency(self):
        start_time = time.time()
        for i in range(100):
            r = self.session.post('http://%s:6060/order' % self.frontAddr,
                                  data={'stockName': "FishCo", 'quantity': 1, 'type': 'sell'})
        end_time = time.time()
        avg_time = (end_time - start_time) / 100
        print("average running time for order is " + str(avg_time))

    def test(self,num):
        if num == 1:
            self.lookupLatency()
        elif num == 2:
            self.tradeLatency()

if __name__ == '__main__':
    FRONTADDRESS = "127.0.0.1"
    stocks = ["GameStart", "FishCo", "BoarCo", "MenhirCo"]
    url = 'http://%s:6060/lookUp/' % FRONTADDRESS
    p = 0.5
    client = Client(p, stocks, url, FRONTADDRESS)
    # client.run()
    start_time = time.time()
    Thread(target=client.test(2)).start()
    Thread(target=client.test(2)).start()
    Thread(target=client.test(2)).start()
    Thread(target=client.test(2)).start()
    Thread(target=client.test(2)).start()

    end_time = time.time()
    avg_time = (end_time - start_time)
    print("time for look up is " + str(avg_time))

