import wave

import pyaudio


class AudioHandler:
    def __init__(self):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100
        self.p = pyaudio.PyAudio()

    def send_audio(self, socket):
        filename = input("Nombre del archivo de audio a guardar (ej: nota.wav): ")
        self.record_audio(filename)
        print(f"Audio guardado como {filename}. Enviando al servidor...")

        # Lee el archivo como bytes
        with open(filename, "rb") as f:
            audio_bytes = f.read()

        # Usa el protocolo para crear el mensaje
        message = Protocol.create_audio_message(audio_bytes)
        socket.sendall(message)
        print("Audio enviado al servidor.")
        
    def record_audio(self, filename):
        print("Recording... (Ctrl+C para detener)")
        stream = self.p.open(format=self.sample_format, channels=self.channels,
                              rate=self.fs, frames_per_buffer=self.chunk, input=True)
        frames = []

        try:
            while True:
                data = stream.read(self.chunk)
                frames.append(data)
        except KeyboardInterrupt:
            print("Recording stopped.")

        stream.stop_stream()
        stream.close()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(frames))

    def play_audio(self, filename):
        print("Playing audio...")
        wf = wave.open(filename, 'rb')
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True)

        data = wf.readframes(self.chunk)
        while data:
            stream.write(data)
            data = wf.readframes(self.chunk)

        stream.stop_stream()
        stream.close()
        wf.close()

    def __del__(self):
        self.p.terminate()