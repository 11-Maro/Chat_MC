class MessageHistory:
    def __init__(self):
        self.history = []

    def add_message(self, message):
        self.history.append(message)

    def get_history(self):
        return self.history

    def save_history(self, file_path):
        with open(file_path, 'w') as file:
            for message in self.history:
                file.write(f"{message}\n")

    def load_history(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.history = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.history = []  # If the file does not exist, start with an empty history.