import binascii
import errno
import hashlib
import json
import logging
import os
import socket
import threading
import time
import socketserver

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9090
while True:
    try:
        sock.bind(('', port))
        print("Сервер запущен на порту -", port)
        logging.info(f"Сервер запущен на порту - {port}")
        break
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("Порт уже занят!")
            port += 1
            logging.warning(f"Порт уже занят, изменение на порт номер: {port}")
        else:
            print("Ошибка в подключении! ", e)
            logging.error(f"Ошибка в подключении! {e}")

# while True:
#     data, address = sock.recvfrom(1024)


# sock.listen(1)

# HTTP = "HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\n\n"


class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        conn, addr = sock.accept()

        # serve up an infinite stream
        i = 0
        while True:
            conn.send("%i " % i)
            time.sleep(0.1)
            i += 1

# [Server() for i in range(100)]
# time.sleep(9e9)
