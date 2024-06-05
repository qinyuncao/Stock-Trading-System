import json
import requests
import random


class Client:
    def __init__(self, p, stocks, url, frontAddr):
        self.session = requests.Session()
        self.p = p
        self.stockName = stocks
        self.url = url
        self.frontAddr = frontAddr

    def run(self):
        self.lookUpAndOrder()
        # while 1:
        #     message = input('run(y/n):')
        #     if str(message) == 'y':
        #         self.lookUpAndOrder()
        #     else:
        #         print("Wrong Code!!!")

    # Look up then buy random number of stock
    def lookUpAndOrder(self):

        r = requests.get(url=self.url + self.stockName[random.randint(0, 9)]).json()  # send request to front end
        print(r)
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
            print(type(data))
            print(data)
            r2 = requests.post('http://%s:6060/order' % self.frontAddr,
                               json=data, headers=headers)
            print(r2.json())


if __name__ == '__main__':
    FRONTADDRESS = "127.0.0.1"
    stocks = ["GameStart", "FishCo", "BoarCo", "MenhirCo", "Gogle", "Mata", "Azon", "Tela", "FAANG", "Appl"]
    url = 'http://%s:6060/lookUp?stockName=' % FRONTADDRESS
    p = 1
    client = Client(p, stocks, url, FRONTADDRESS)
    client.run()
