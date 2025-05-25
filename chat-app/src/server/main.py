import socket
import threading

from group import GroupChat
from message import MessageStorage
from src.utils.protocol import Protocol


class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = []
        self.message_handler = MessageStorage()
        self.group_manager = GroupChat()

    def handle_client(self, client_socket, address):
        print(f"Connection from {address} has been established.")
        self.clients.append(client_socket)

        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    self.process_message(message, client_socket)
                else:
                    break
            except ConnectionResetError:
                break

        client_socket.close()
        self.clients.remove(client_socket)
        print(f"Connection from {address} has been closed.")

    def process_message(self, message, client_socket):
        # Process the incoming message based on the protocol
        protocol = Protocol()
        command, data = protocol.parse_message(message)
        
        if command == 'SEND_MESSAGE':
            self.message_handler.save_message(data)
            self.broadcast_message(data, client_socket)
        elif command == 'CREATE_GROUP':
            self.group_manager.create_group(data)
        if command == 'AUDIO':
            # Guarda el audio recibido en un archivo
            filename = f"audio_{threading.get_ident()}.wav"
            with open(filename, "wb") as f:
                f.write(data.encode('latin1') if isinstance(data, str) else data)
            print(f"Audio recibido y guardado como {filename}")
            # Puedes guardar en el historial si lo deseas:
            self.message_handler.save_audio_message("unknown", "unknown", filename)

    def broadcast_message(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                client.send(message.encode('utf-8'))

    def start(self):
        print("Server is running...")
        while True:
            client_socket, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            client_thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()