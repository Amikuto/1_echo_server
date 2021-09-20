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


def add_new_user(address, pwd, name):
    with open("users.json", "r") as f:
        js_file = json.load(f)

    target = js_file["users"]
    user_info = {name: {'password': hash_password(pwd), 'address': address}}
    target.update(user_info)

    with open("users.json", "w") as file:
        json.dump(js_file, file, indent=4)


def check_if_exist(name):
    with open("users.json", "r") as f:
        temp = json.load(f)
        if temp["users"][name]:
            return True
        else:
            return False


def getpass(name):
    with open("users.json", "r") as f:
        temp = json.load(f)
        passwd = temp["users"][name]["password"]
    return passwd


# add_new_user("192.161.0.19", hash_password("123"), "test1")
# add_new_user("192.161.0.19", hash_password("123"), "test2")
# print(check_if_exist("test1"))

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
    msg = ''
    conn, addr = sock.accept()
    print("Пользователь подключен!")
    print(addr)
    logging.info(f"Пользователь подключен! {addr}")

    text = "Введите логин: "
    conn.send(text.encode())
    login = conn.recv(1024).decode()
    conn.send(f"Ваш логин {login}... Теперь введите пароль: ".encode())
    password = conn.recv(1024).decode()

    flag = False

    try:
        if check_if_exist(login):
            while not flag:
                if verify_password(getpass(login), password):
                    flag = True
                    conn.send("Вход успешно выполнен. Теперь сервер будет отвечать на ваши сообщения!".encode())
                    break
                else:
                    conn.send("Пароль неверен, введите его заново: ".encode())
                    password = conn.recv(1024).decode()
    except KeyError:
        conn.send("Увы, такого пользователя нет в базе. Добавление по введенному логину и паролю...".encode())
        add_new_user(addr[0], password, login)

    while True:
        print("Начался прием данных от клиента!")
        logging.info("Начался прием данных от клиента!")
        data = conn.recv(1024)
        if data.decode() == "exit":
            print("Завершение соединения с клиентом!")
            logging.info("Завершение соединения с клиентом!")
            conn.close()
            break
        msg += data.decode()

        print("Началась отправка данных клиенту!")
        logging.info(f"Началась отправка данных клиенту! {data.decode()}")
        conn.send(data)
