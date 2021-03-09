import socket
from time import sleep

sock = socket.socket()
print("Начало соединения с сервером!")
address = input("Введите адрес для подключения: ")
if not address or address == '':
    address = "localhost"

port = input("Введите номер порта: ")
if not port or port == '':
    port = 9090
sock.connect(('localhost', 9090))

connection = True

while True:
    send = input()
    msg = send
    print("Началась отправка данных серверу!")
    sock.send(msg.encode())

    print("Прием данных от сервера!")
    data = sock.recv(1024)

    # sock.close()

    if data.decode() == "exit":
        sock.close()
        break

    print(data.decode())
