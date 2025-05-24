import threading
from socket import AF_INET, SOCK_STREAM, socket


class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.server_address = (host, port)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.server_address)
        self.username = input("Enter your username: ")
        self.running = True

    def send_message(self, message):
        self.client_socket.sendall(f"{self.username}: {message}".encode('utf-8'))

    def receive_messages(self):
        while self.running:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    print(message)
                else:
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def start_chat(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()
        while self.running:
            message = input()
            if message.lower() == 'exit':
                self.running = False
                self.client_socket.close()
            else:
                self.send_message(message)


    def create_group(self, group_name):
        # Envía comando al servidor para crear grupo
        self.client_socket.sendall(f"CREATE_GROUP:{group_name}".encode('utf-8'))
                
    def join_group(self, group_name):
        # Envía comando al servidor para unirse a grupo
        self.client_socket.sendall(f"JOIN_GROUP:{group_name}".encode('utf-8'))

if __name__ == "__main__":
    chat_client = ChatClient()
    chat_client.start_chat()