import socket
import threading

HOST, PORT = "192.168.8.8", 42069


def send_request(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data, "utf-8"))


def receive_messages():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print("\n" + data.decode("utf-8"))


# Start a separate thread for receiving messages
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

# Main thread for sending messages
while True:
    message = input()
    send_request(message)
