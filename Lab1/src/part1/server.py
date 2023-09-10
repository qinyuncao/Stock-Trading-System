import socket
from classes import ThreadPool

# our database
stock_list = {
    'GameStart': {'price': 15.99, 'volume': 5},
    'FishCo': {'price': 10.28, 'volume': 2}
}
ThreadPool = ThreadPool(5, stock_list) # Establish the thread pool


def run():
    s = socket.socket()
    host = socket.gethostname()  # Get local machine name
    port = 9997  # Reserve a port for your service
    BUFFER_SIZE = 1024
    s.bind((host, port))  # Bind to the port
    s.listen(5)  # Now wait for client connection

    while True:
        c, addr = s.accept()  # Establish connection with client
        print(f"Connection from {addr} has been established.")
        c.send('Thank you for connecting.'.encode())
        message = c.recv(BUFFER_SIZE).decode('utf-8')
        print(message)
        name = message.split(" ")[2]
        ThreadPool.add(name, c)
    return


if __name__ == "__main__":
    run()
