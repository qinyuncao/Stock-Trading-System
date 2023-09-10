import socket
import concurrent.futures
import time


def lookupAveTime():
    start_t1 = time.time()
    for i in range(100):
        s = socket.socket()
        host = socket.gethostname()  # Get local machine host name
        port = 9997  # Specify the port to connect to
        BUFFER_SIZE = 1024
        s.connect((host, port))
        s.recv(BUFFER_SIZE).decode('utf-8')
        # Get all three possibility equally
        if i % 3 == 0:
            stock_name = "GameStart"
        elif i % 3 == 1:
            stock_name = "FishCo"
        else:
            stock_name = "test"

        MESSAGE = "Please lookup " + stock_name
        s.send(MESSAGE.encode())
        # print(s.recv(BUFFER_SIZE).decode('utf-8'))
        s.close()  # Close the socket when done
    end_t1 = time.time()
    result = (end_t1 - start_t1) / 100
    print("average time for lookup in 100 times is " + str(result))


with concurrent.futures.ThreadPoolExecutor() as executer:
    result = [executer.submit(lookupAveTime()) for _ in range(5)]

