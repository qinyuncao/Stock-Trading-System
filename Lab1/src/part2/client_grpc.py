import concurrent.futures

import grpc
import stockSystem_pb2 as pb2
import stockSystem_pb2_grpc as pb2_grpc
from dataset import *
import random
import time
import concurrent.futures


class stockSystemClient(object):
    def __init__(self):
        self.host = local_host
        self.port = port

        # instantiate a channel
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.port))

        # bind the client and the server
        self.stub = pb2_grpc.stockSystemStub(self.channel)

    def lookup_client(self, name):
        """
        Client function to call the rpc for Lookup
        """
        request = pb2.stockName(stock_name=name)
        price = self.stub.Lookup(request).stock_price
        volume = self.stub.Lookup(request).stock_volume
        return [price, volume]

    def trade_client(self, name, n, type):
        """
        Client function to call the rpc for Trade
        """
        request = pb2.tradingRequest(stock_name=name, num=n, trade_type=type)
        return self.stub.Trade(request).status_indicator

    def update_client(self, name, price):
        """
        Client function to call the rpc for Update
        """
        request = pb2.updateRequest(stock_name=name, stock_price=price)
        return self.stub.Update(request).status_indicator


# This is the special client for random update stock's price every 1 second
def random_Client(times):
    for i in range(times):
        ran_c = stockSystemClient()
        random_number = random.randint(0, 100)
        random_price = random.randint(1, 100)
        if random_number % 4 == 0:
            ran_c.update_client("GameStart", random_price)
        if random_number % 4 == 1:
            ran_c.update_client("FishCo", random_price)
        if random_number % 4 == 2:
            ran_c.update_client("BoarCo", random_price)
        if random_number % 4 == 3:
            ran_c.update_client("MenhirCo", random_price)
        time.sleep(1)


def lookUpAveT():
    start_t1 = time.time()
    for i in range(100):
        client = stockSystemClient()
        client.lookup_client("FishCo")
    end_t1 = time.time()
    ave_lookup_t = (end_t1 - start_t1) / 100
    print("average time for lookup in 100 times is " + str(ave_lookup_t))


def tradeAveT():
    start_t2 = time.time()
    for i in range(100):
        client = stockSystemClient()
        client.trade_client("FishCo", 10, "buy")
    end_t2 = time.time()
    ave_trade_t = (end_t2 - start_t2) / 100
    print("average time for trade in 100 times is " + str(ave_trade_t))


def updateAveT():
    start_t3 = time.time()
    for i in range(100):
        client = stockSystemClient()
        client.update_client("FishCo", i)
    end_t3 = time.time()
    ave_update_t = (end_t3 - start_t3) / 100
    print("average time for update in 100 times is " + str(ave_update_t))


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executer:
        result = [executer.submit(lookUpAveT()) for _ in range(5)]
    with concurrent.futures.ThreadPoolExecutor() as executer:
        result = [executer.submit(tradeAveT()) for _ in range(5)]
    with concurrent.futures.ThreadPoolExecutor() as executer:
        result = [executer.submit(updateAveT()) for _ in range(5)]

    # client = stockSystemClient()
    # updating_client = stockSystemClient()
    # action = input("Please enter the actions you'd like to take (lookup, trade or update): ")
    # name = input("Please enter the name of the stock: ")
    #
    # if action == "lookup":
    #     res = client.lookup_client(name)
    #     print("The price of the stock is : " + str(res[0]))
    #     print("The trading volume of the stock is : " + str(res[1]))
    #
    # elif action == "trade":
    #     type = input("Please enter the actions you'd like to take (buy or sell): ")
    #     num = int(input("Please enter the number of the stocks you'd like to trade: "))
    #     res = client.trade_client(name, num, type)
    #     if res == 1:
    #         print("Trading completed.")
    #     if res == 0:
    #         print("Trading is suspended.")
    #     if res == -1:
    #         print("An invalid stock name is specified.")
    #
    # elif action == "update":
    #     price = int(input("Please enter the new price of the stock: "))
    #     res = client.update_client(name, price)
    #     if res == 1:
    #         print("Update is successful.")
    #     if res == -2:
    #         print("An incalid price is specified.")
    #     if res == -1:
    #         print("An invalid stock name is specified.")
    #
    # else:
    #     print("Wrong actions entered")
    #
    # random_Client(5)
