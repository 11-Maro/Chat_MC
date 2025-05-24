import socket
import threading

from audio import AudioHandler
from call import CallClient
from chat import ChatClient


class Client:
    def __init__(self, host='localhost', port=12345):
        self.server_address = (host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat = ChatClient(host, port)
        self.audio = AudioHandler()
        self.call = CallClient(self.server_address)

    def connect(self):
        try:
            self.socket.connect(self.server_address)
            print("Connected to the server.")
            self.listen_for_messages()
        except Exception as e:
            print(f"Connection failed: {e}")

    def listen_for_messages(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    print(f"Message from server: {message}")
                else:
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def run(self):
        self.connect()
        while True:
            user_input = input("Enter a command (text/audio/call/exit): ")
            if user_input == "text":
                msg = input("Escribe tu mensaje: ")
                self.chat.send_message(msg)
            elif user_input == "audio":
                self.audio.send_audio(self.socket)
            elif user_input == "call":
                self.call.initiate_call()
            elif user_input == "exit":
                self.socket.close()
                break
            else:
                print("Unknown command.")

if __name__ == "__main__":
    client = Client()
    client.run()