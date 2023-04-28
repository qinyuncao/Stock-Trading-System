import socket
import json
from threading import Lock, Thread

from dataSettings import *
import os

cAddr = catalogService_addr
oAddr = orderService_addr
cSAddr = (os.getenv("PG_HostC", "127.0.0.1"), 7090)
lock = Lock()
count1 = -1
count2 = -1
count3 = -1


# Process POST from front end （'POST {trade} {num} {name}'）
def trade(c, msg,port):
    tradeType = msg.split(' ')[1]
    quantity = msg.split(' ')[2]
    stockName = msg.split(' ')[3]
    order_msg = 'order {tradeType} {quantity} {stock_name}'.format(tradeType=tradeType, quantity=quantity,
                                                                   stock_name=stockName)
    s = socket.socket()
    s.connect(cSAddr)
    s.send(order_msg.encode())
    indicator = s.recv(1024).decode('utf-8')
    s.close()
    print(indicator)

    if indicator == '400':
        payload = json.dumps(
            {
                "error": {
                    "code": 400,
                    "message": "trade is invalid"
                }
            }
        )
        reply_msg = '{code}/{payload}'.format(code=400, payload=payload)
        c.send(reply_msg.encode())

    elif indicator == '200':
        payload = json.dumps(
            {
                "data": {
                    "transaction number": quantity,
                }
            }
        )
        reply_msg = '{code}/{payload}'.format(code=200, payload=payload)
        c.send(reply_msg.encode())

        curr_counter = -1
        if port == 6000:
            curr_counter = count1+1
        elif port == 6001:
            curr_counter = count2+1
        elif port == 6002:
            curr_counter = count3+1


        order_history = curr_counter + ' stockName:' + stockName + ",tradeType:" + tradeType + ",quantity:" + str(quantity) + '\n'
        file = "order"+str(port)+".txt"
        with open(file, 'w+') as file:
            # write some text to the file
            file.write(order_history)

        #给其他follower发消息


#可能有order, leader通知(从frontend），leader给follower发消息，healthcheck（从frontend和从order到order),crash掉以后的同步申请
def handle_client(client_socket,port):
    # code to handle client requests
    request = client_socket.recv(1024).decode('utf-8')
    action = request.splitlines()[0].split(' ')[0]
    if action == 'order':
        trade(client_socket, request,port)
    elif action == 'asldfkja':
        #other actions

    return


def start_server(port):
    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a specific address and port
    server_socket.bind(('localhost', port))

    # listen for incoming connections
    server_socket.listen(1)

    # accept incoming connections and handle them in separate threads
    while True:
        client_socket, address = server_socket.accept()
        client_thread = Thread(target=handle_client, args=(client_socket,port))
        client_thread.start()

if __name__ == '__main__':
    #port = 9090 改frontend

    # start multiple servers in separate threads
    server_threads = []
    for port in range(6000, 6003):
        filename = "order" + str(port) + ".txt"
        if os.path.exists(filename):
            if port == 6000:
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    for line in reversed(lines):
                        if int(line.split(' ')[0]) > 0:
                            count1 = int(line.split(' ')[0])
            elif port == 6001:
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    for line in reversed(lines):
                        if int(line.split(' ')[0]) > 0:
                            count2 = int(line.split(' ')[0])
            elif port == 6002:
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    for line in reversed(lines):
                        if int(line.split(' ')[0]) > 0:
                            count3 = int(line.split(' ')[0])
        else:
            if port == 6000:
                count1 = 0
            elif port == 6001:
                count2 = 0
            elif port == 6002:
                count2 = 0

        server_thread = Thread(target=start_server, args=(port,))
        server_thread.start()
        server_threads.append(server_thread)

    # wait for all threads to finish
    for server_thread in server_threads:
        server_thread.join()
