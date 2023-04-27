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

        r = requests.get(url=self.url + self.stockName[random.randint(0, 3)]).json()  # send request to front end
        reply = json.loads(r)
        print(reply)
        stockName, quantity = reply['data']['stockName'], reply['data']['quantity']

        # If stock has more than 0 and probability is less than p
        if quantity > 0 and random.random() < self.p:
            randomBuy = random.randint(1, 1000)
            if random.random() < self.p:
                tradeType = "buy"
            else:
                tradeType = "sell"
            r2 = self.session.post('http://%s:6060/order/' % self.frontAddr,
                                   data={'stockName': stockName, 'quantity': randomBuy, 'type': tradeType})
            print(r2.json())


if __name__ == '__main__':
    FRONTADDRESS = "127.0.0.1"
    stocks = ["GameStart", "FishCo", "BoarCo", "MenhirCo"]
    url = 'http://%s:6060/lookUp?stockName=' % FRONTADDRESS
    p = 0.5
    client = Client(p, stocks, url, FRONTADDRESS)
    client.run()
