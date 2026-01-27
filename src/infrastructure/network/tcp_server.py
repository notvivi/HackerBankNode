import socket
import threading
from infrastructure.network.tcp_handler import handle_client
import logging


class TCPServer:
    def __init__(self, host: str, port: int, factory, timeout: int = 5, max_connections: int = 100):
        self.host = host
        self.port = port
        self.factory = factory
        self.timeout = timeout
        self.max_connections = max_connections
        self.running = False

    def start(self):
        self.running = True

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((self.host, self.port))
        server_socket.listen(self.max_connections)

        logging.info(f"Bank node listening on {self.host}:{self.port}")

        while self.running:
            try:
                client_socket, addr = server_socket.accept()

                logging.info(f"Connection from {addr}")

                client_socket.settimeout(self.timeout)

                thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, addr, self.factory, self.timeout),
                    daemon=True
                )
                thread.start()

            except Exception as e:
                logging.error(f"Server error: {e}")

    def stop(self):
        self.running = False

