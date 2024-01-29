import socketserver
import threading

connection_pool = []
lock = threading.Lock()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def send_to_all(data, source_address):
    with lock:
        for client_socket in connection_pool.copy():
            if client_socket.getpeername() != source_address:
                try:
                    client_socket.sendall(bytes(f"{source_address}: {data}", "utf-8"))
                except Exception:
                    # Remove the client if unable to send message
                    connection_pool.remove(client_socket)


class ChatRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        with lock:
            if self.request not in connection_pool:
                connection_pool.append(self.request)
        while True:
            data = self.request.recv(1024)
            if not data:
                # Connection closed by the client
                with lock:
                    connection_pool.remove(self.request)
                break
            print(data.decode("utf-8"))
            send_to_all(data.decode("utf-8"), self.request.getpeername())


server = ThreadedTCPServer(("0.0.0.0", 42069), ChatRequestHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()
server_thread.join()
