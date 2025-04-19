import socket
import threading
import time

class Peer:
    def __init__(self, host, port, bootstrap_nodes=[]):
        self.host = host
        self.port = port
        self.bootstrap_nodes = bootstrap_nodes  # Список начальных узлов
        self.peers = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Узел запущен на {self.host}:{self.port}")

    def start(self):
        # Поток для прослушивания входящих подключений
        listener_thread = threading.Thread(target=self._listen)
        listener_thread.start()

        # Подключение к bootstrap-узлам
        self._connect_to_bootstrap_nodes()

        # Отправка сообщений
        while True:
            message = input("Введите сообщение: ")
            self._broadcast(message)

    def _listen(self):
        while True:
            client, addr = self.server.accept()
            print(f"Подключен новый узел: {addr}")
            self.peers.append(client)
            handler_thread = threading.Thread(target=self._handle_client, args=(client,))
            handler_thread.start()

    def _handle_client(self, client):
        while True:
            try:
                data = client.recv(1024).decode('utf-8')
                if data:
                    print(f"\nПолучено сообщение: {data}")
            except:
                client.close()
                break

    def _connect_to_bootstrap_nodes(self):
        for node in self.bootstrap_nodes:
            host, port = node
            try:
                peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                peer.connect((host, port))
                self.peers.append(peer)
                print(f"Подключен к bootstrap-узлу {host}:{port}")
            except:
                print(f"Ошибка подключения к {host}:{port}")

    def _broadcast(self, message):
        for peer in self.peers:
            try:
                peer.send(message.encode('utf-8'))
            except:
                self.peers.remove(peer)

bootstrap_node = Peer('localhost', 5000)
bootstrap_node.start()

node2 = Peer('localhost', 5001, bootstrap_nodes=[('localhost', 5000)])
node2.start()

node3 = Peer('localhost', 5002, bootstrap_nodes=[('localhost', 5000)])
node3.start()
