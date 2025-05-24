import socket
import threading

class CallClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.socket.connect(self.server_address)
            self.connected = True
            print("Connected to the server for calls.")
        except Exception as e:
            print(f"Failed to connect to the server: {e}")

    def initiate_call(self, recipient):
        if self.connected:
            message = f"CALL {recipient}"
            self.socket.sendall(message.encode())
            print(f"Call initiated to {recipient}.")
        else:
            print("Not connected to the server.")

    def receive_calls(self):
        while self.connected:
            try:
                message = self.socket.recv(1024).decode()
                if message.startswith("CALL"):
                    caller = message.split()[1]
                    print(f"Incoming call from {caller}.")
                    # Here you would add logic to accept or reject the call
            except Exception as e:
                print(f"Error receiving call: {e}")
                self.connected = False

    def close(self):
        self.socket.close()
        self.connected = False
        print("Disconnected from the server.")

def main():
    server_address = ('localhost', 5000)  # Replace with your server address
    call_client = CallClient(server_address)
    call_client.connect()

    threading.Thread(target=call_client.receive_calls, daemon=True).start()

    # Example usage
    while True:
        command = input("Enter command (call <username> or exit): ")
        if command.startswith("call"):
            _, recipient = command.split()
            call_client.initiate_call(recipient)
        elif command == "exit":
            call_client.close()
            break

if __name__ == "__main__":
    main()