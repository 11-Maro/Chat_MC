# protocol.py

class Protocol:
    HEADER_SIZE = 10

    @staticmethod
    def create_message(message_type, content):
        message = f"{message_type:<{Protocol.HEADER_SIZE}}{content}"
        return message.encode('utf-8')

    @staticmethod
    def parse_message(data):
        message_type = data[:Protocol.HEADER_SIZE].decode('utf-8').strip()
        content = data[Protocol.HEADER_SIZE:].decode('utf-8')
        return message_type, content

    @staticmethod
    def create_audio_message(audio_data):
        return Protocol.create_message("AUDIO", audio_data)

    @staticmethod
    def create_text_message(text):
        return Protocol.create_message("TEXT", text)

    @staticmethod
    def create_call_request(caller_id, receiver_id):
        return Protocol.create_message("CALL", f"{caller_id}:{receiver_id}")

    @staticmethod
    def create_group_message(group_id, content):
        return Protocol.create_message("GROUP", f"{group_id}:{content}")