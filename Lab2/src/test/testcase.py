import json
import socket
import requests
import unittest

cAddr = ('127.0.0.1', 7090)
oAddr = ('127.0.0.1', 9090)
fAddr = ('127.0.0.1', 6060)
f_url_lookup = 'http://127.0.0.1:6060/lookUp/'
f_url_order = 'http://127.0.0.1:6060/'

class TestCases(unittest.TestCase):

    def testOrderSell(self):
        s = socket.socket()
        s.connect(oAddr)
        order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType="sell", quantity=10,
                                                                     stock_name="FishCo")
        s.send(order_msg.encode())
        order_response = s.recv(1024).decode('utf-8')
        s.close()
        res_msg = order_response.split('/')[1]
        expect_trans = "10"
        reply = json.loads(res_msg)
        trans = reply['data']['transaction number']
        self.assertEqual(trans, expect_trans)

    def testOrderBuy(self):
        s = socket.socket()
        s.connect(oAddr)
        order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType="buy", quantity=10,
                                                                     stock_name="FishCo")
        s.send(order_msg.encode())
        order_response = s.recv(1024).decode('utf-8')
        s.close()
        res_msg = order_response.split('/')[1]
        expect_trans = "10"
        reply = json.loads(res_msg)
        trans = reply['data']['transaction number']
        self.assertEqual(trans, expect_trans)

    def testOrderBuyTooMuch(self):
        s = socket.socket()
        s.connect(oAddr)
        order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType="buy", quantity=100000000000,
                                                                     stock_name="FishCo")
        s.send(order_msg.encode())
        order_response = s.recv(1024).decode('utf-8')
        s.close()
        res_msg = order_response.split('/')[1]
        expect_code = 400
        expect_msg = "trade is invalid"
        reply = json.loads(res_msg)
        code, message = reply['error']['code'],reply['error']['message']
        self.assertEqual(code, expect_code)
        self.assertEqual(message, expect_msg)

    #Since the quantity might change, we only check stock name and price in look up
    def testFrontendLookUp(self):
        s = requests.session()
        r = s.get(f_url_lookup+"FishCo").json()
        reply = json.loads(r)
        stockName, price = reply['data']['stockName'], reply['data']['price']
        expect_stockName = "FishCo"
        expect_price = 10.98

        self.assertEqual(stockName, expect_stockName)
        self.assertEqual(price, expect_price)

    def testFrontendLookUpNotFound(self):
        s = requests.session()
        r = s.get(f_url_lookup+"NotFound").json()
        reply = json.loads(r)
        code, message = reply['error']['code'], reply['error']['message']
        expect_code = 404
        expect_msg = "stock not found"

        self.assertEqual(code, expect_code)
        self.assertEqual(message, expect_msg)


    def testFrontendSell(self):
        s = requests.session()
        r = s.post(f_url_order,data={'stockName': "FishCo", 'quantity': 10, 'type': "sell"}).json()
        reply = json.loads(r)
        expect_trans = "10"
        trans = reply['data']['transaction number']
        self.assertEqual(trans, expect_trans)

    def testFrontendBuyTooMuch(self):
        s = requests.session()
        r = s.post(f_url_order,data={'stockName': "FishCo", 'quantity': 1000000000000, 'type': "buy"}).json()
        reply = json.loads(r)
        expect_code = 400
        expect_msg = "trade is invalid"
        code, message = reply['error']['code'], reply['error']['message']
        self.assertEqual(code, expect_code)
        self.assertEqual(message, expect_msg)






if __name__ == '__main__':
    unittest.main()
