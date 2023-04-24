import socket
import json
from threading import Thread
from dataSettings import *
import os
fAddr = frontEndService_addr
oAddr = orderService_addr
cAddr = catalogService_addr
oSAddr = (os.getenv("PG_HostO","127.0.0.1"), 9090)
cSAddr = (os.getenv("PG_HostC","127.0.0.1"), 7090)

class frontEnd:
    def __init__(self, *args, **kwargs):
        pass

    # Recived GET request from client and forward it to Catalog_Service
    def get_request(self, c, request):
        msg = request.splitlines()[0].split(' ')[1]
        stock = msg.split('/')[2]

        s = socket.socket()
        s.connect(cSAddr)
        lookup_msg = 'Lookup {stock_name}'.format(stock_name=stock)
        s.send(lookup_msg.encode())
        lookup_response = s.recv(1024).decode('utf-8')
        s.close()

        status_code = lookup_response.split('/')[0]
        res_msg = lookup_response.split('/')[1]

        if status_code == "200":
            reply = json.dumps(res_msg)
            c.send(
                response.format(status_code=200, status_msg='OK', content_length=len(reply), payload=reply).encode(
                    "utf-8"))
        else:
            reply = json.dumps(res_msg)
            c.send(
                response.format(status_code=404, status_msg='Error', content_length=len(reply), payload=reply).encode(
                    "utf-8"))
        c.close()

    # Process POST request from client
    # Request is in JSON
    def post_request(self, c, request):
        print(request)
        print(request.splitlines()[-1])
        print(request.splitlines()[-1].split('&')[0])
        print(request.splitlines()[-1].split('&')[0].split('=')[1])
        stockName = request.splitlines()[-1].split('&')[0].split('=')[1]
        quantity = request.splitlines()[-1].split('&')[1].split('=')[1]
        tradeType = request.splitlines()[-1].split('&')[2].split('=')[1]
        s = socket.socket()
        s.connect(oSAddr)
        order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType=tradeType, quantity=quantity,
                                                                     stock_name=stockName)
        s.send(order_msg.encode())
        order_response = s.recv(1024).decode('utf-8')
        s.close()

        status_code = order_response.split("/")[0]
        res_msg = order_response.split("/")[1]
        if status_code == "200":
            reply = json.dumps(res_msg)
            c.send(
                response.format(status_code=200, status_msg='OK', content_length=len(reply), payload=reply).encode(
                    "utf-8"))
        else:
            reply = json.dumps(res_msg)
            c.send(
                response.format(status_code=400, status_msg='Error', content_length=len(reply), payload=reply).encode(
                    "utf-8"))
        c.close()
        
    def frontEndHandler(self, c):
        request = c.recv(1024).decode('utf-8')

        action = request.splitlines()[0].split(' ')[0]
        if action == 'GET':
            self.get_request(c, request)
        if action == 'POST':
            self.post_request(c, request)
        return
    

    # lab3从这里开始！！！！！！！！！




if __name__ == '__main__':
    front_end = frontEnd()
    s = socket.socket()
    port = 6060
    s.bind((fAddr,port))
    s.listen(5)
    while True:
        c, addr = s.accept()  # Establish connection with client
        Thread(target=front_end.frontEndHandler, args=(c,)).start()
