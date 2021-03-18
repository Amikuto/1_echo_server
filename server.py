import binascii
import errno
import hashlib
import json
import logging
import os
import socket


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def add_new_user(address, password, name):
    info = {
        name:
            {
                "address": address,
                "password": hash_password(password)
            }
    }

    with open("users.json", "w") as f:
        json.dump(info, f)


def getpass(name):
    with open("users.json", "r") as f:
        temp = json.load(f)
        passwd = temp[name]["password"]
    return passwd


# add_new_user("192.161.0.19", "123", "damir")
#
# print(verify_password(getpass("damir"), "123"))

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='logs.log')
connection_dic = {}

sock = socket.socket()

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

sock.listen(0)
print("Начало прослушивания порта!")
logging.info("Начало прослушивания порта!")

while True:
    conn, addr = sock.accept()
    print("Пользователь подключен!")
    print(addr)
    logging.info(f"Пользователь подключен! {addr}")

    text = "Введите логин: "
    conn.send(text.encode())
    login = conn.recv(1024).decode()
    conn.send(f"Ваш логин {login}... Теперь введите пароль: ".encode())
    password = conn.recv(1024).decode()

    if verify_password(getpass(login), password):
        conn.send("Вход успешно выполнен".encode())
    else:
        conn.send("Увы, либо пароль неверен, либо такого пользователя нет в базе".encode())

    # if addr in connection_dic:
    #     text = "Приветствую, пользователь " + connection_dic.get(addr)
    #     conn.send(text.encode())
    # else:
    #     conn.send("Введите имя пользователя дял регистрации на сервере: ".encode())
    #     connection_dic[addr[0]] = conn.recv(1024).decode()

    # msg = ''

    # while True:
    #     print("Начался прием данных от клиента!")
    #     logging.info("Начался прием данных от клиента!")
    #     data = conn.recv(1024)
    #     if data.decode() == "exit":
    #         print("Завершение работы сервера!")
    #         logging.info("Завершение работы сервера!")
    #         conn.close()
    #         break
    #     msg += data.decode()
    #
    #     print("Началась отправка данных клиенту!")
    #     logging.info(f"Началась отправка данных клиенту! {data.decode()}")
    #     conn.send(data)
