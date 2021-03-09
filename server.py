import errno
import socket
import logging


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='logs.log')

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

	msg = ''

	while True:
		print("Начался прием данных от клиента!")
		logging.info("Начался прием данных от клиента!")
		data = conn.recv(1024)
		if data.decode() == "exit":
			print("Завершение работы сервера!")
			logging.info("Завершение работы сервера!")
			conn.close()
			break
		msg += data.decode()

		print("Началась отправка данных клиенту!")
		logging.info(f"Началась отправка данных клиенту! {data.decode()}")
		conn.send(data)
