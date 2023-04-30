import time
import requests
import random
from threading import Thread
import json


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
    def lookupAndOrderLatency(self):
        start_time = time.time()
        order_numeber = []
        for i in range(1):
            r = self.session.get(url=self.url + self.stockName[random.randint(0, 3)]).json()
            reply = json.loads(r)
            stockName, quantity = reply['data']['stockName'], reply['data']['quantity']

            # If stock has more than 0 and probability is less than p
            if quantity > 0 and random.random() < self.p:
                randomBuy = random.randint(1, 1000)
                if random.random() < self.p:
                    tradeType = "buy"
                else:
                    tradeType = "sell"
                headers = {
                    "Content-Type": "application/json"
                }
                data = json.dumps({'stockName': stockName, 'quantity': randomBuy, 'type': tradeType})
                r2 = requests.post('http://%s:6060/order' % self.frontAddr,
                                   json=data, headers=headers).json()
                reply2 = json.loads(r2)
                print(reply2)
        end_time = time.time()
        avg_time = (end_time - start_time) / 100
        print("average running time for look up is " + str(avg_time))


if __name__ == '__main__':
    FRONTADDRESS = "127.0.0.1"
    stocks = ["GameStart", "FishCo", "BoarCo", "MenhirCo"]
    url = 'http://%s:6060/lookUp?stockName=' % FRONTADDRESS
    p = 0.5
    client = Client(p, stocks, url, FRONTADDRESS)
    # client.run()
    start_time = time.time()
    Thread(target=client.lookupAndOrderLatency()).start()
    Thread(target=client.lookupAndOrderLatency()).start()
    Thread(target=client.lookupAndOrderLatency()).start()
    Thread(target=client.lookupAndOrderLatency()).start()
    Thread(target=client.lookupAndOrderLatency()).start()

    end_time = time.time()
    avg_time = (end_time - start_time)
    print("time for look up is " + str(avg_time))
