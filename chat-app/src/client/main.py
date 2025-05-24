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
    
    def login(self):
        print("Bienvenido. Selecciona:")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        opcion = input("Opción: ")
        if opcion == "1":
            username = input("Usuario: ")
            password = input("Contraseña: ")
            # Envía credenciales al servidor
        elif opcion == "2":
            username = input("Nuevo usuario: ")
            password = input("Nueva contraseña: ")
            # Envía datos al servidor para registro

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
            print("\nMenú principal:")
            print("1. Enviar mensaje a usuario")
            print("2. Enviar mensaje a grupo")
            print("3. Enviar audio a usuario")
            print("4. Enviar audio a grupo")
            print("5. Crear grupo")
            print("6. Unirse a grupo")
            print("7. Llamar a usuario")
            print("8. Llamar a grupo")
            print("9. Ver historial")
            print("0. Salir")
            user_input = input("Selecciona una opción: ")

            match user_input:
                case "1":
                    recipient = input("Usuario destinatario: ")
                    msg = input("Mensaje: ")
                    self.chat.send_message_to_user(recipient, msg)
                case "2":
                    group = input("Nombre del grupo: ")
                    msg = input("Mensaje: ")
                    self.chat.send_message_to_group(group, msg)
                case "3":
                    recipient = input("Usuario destinatario: ")
                    self.audio.send_audio_to_user(self.socket, recipient)
                case "4":
                    group = input("Nombre del grupo: ")
                    self.audio.send_audio_to_group(self.socket, group)
                case "5":
                    group = input("Nombre del nuevo grupo: ")
                    self.chat.create_group(group)
                case "6":
                    group = input("Nombre del grupo: ")
                    self.chat.join_group(group)
                case "7":
                    recipient = input("Usuario destinatario: ")
                    self.call.initiate_call(recipient)
                case "8":
                    group = input("Nombre del grupo: ")
                    self.call.initiate_group_call(group)
                case "9":
                    self.chat.show_history()
                case "0":
                    self.socket.close()
                    break
                case _:
                    print("Opción no válida.")

if __name__ == "__main__":
    client = Client()
    client.run()