import socket
from time import sleep

sock = socket.socket()
# sock.setblocking(1)
sock.connect(('localhost', 9090))

#msg = input()
# msg = input("Введите текст эха: ")

while True:
    send = input()
    msg = send
    sock.send(msg.encode())

    data = sock.recv(1024)

    # sock.close()

    if data.decode() == "exit":
        sock.close()
        break

    print(data.decode())
