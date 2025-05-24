class MessageStorage:
    def __init__(self):
        self.history = []

    def save_text_message(self, sender, recipient, message):
        entry = {
            'type': 'text',
            'sender': sender,
            'recipient': recipient,
            'message': message,
            'timestamp': self._get_current_timestamp()
        }
        self.history.append(entry)

    def save_audio_message(self, sender, recipient, audio_file_path):
        entry = {
            'type': 'audio',
            'sender': sender,
            'recipient': recipient,
            'audio_file_path': audio_file_path,
            'timestamp': self._get_current_timestamp()
        }
        self.history.append(entry)

    def get_history(self):
        return self.history

    def _get_current_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()