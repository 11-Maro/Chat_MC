# Chat Application README

## Chat_MC

Chat multiple client- text audio gr1 -- Cierre: viernes, 23 de mayo de 2025, 23:59
En grupos de 4: No se aceptan trabajos individuales o grupos de más de 4 personas.

Implementar un chat que permita:

1. Crear grupos de chat.
2. Enviar un mensaje de texto a un usuario en especifico o a un grupo.
3. Enviar una nota de voz a un usuario en especifico o a un grupo.
4. realizar una llamada a un usuario o a un grupo.
5. se debe guardar el historial de mensajes enviados (texto y audios).

Para cada requerimiento debe escoger el protocolo de comunicación (TCP o UDP) más apropiado, la interacción puede ser realizado por linea de comandos o GUI.

Aparte del código fuente, debe entregar un Readme con las instrucciones para ejecutar su programa y el nombre de los integrantes.

This project is a chat application that allows multiple clients to communicate via text messages, audio notes, and voice calls. It also saves the history of messages sent.

### Features

1. Create groups of chat.
2. Send text messages to specific users or groups.
3. Send audio notes to specific users or groups.
4. Make voice calls to specific users or groups.
5. Save the history of sent messages (both text and audio).

### Project Structure

```
chat-app
├── src
│   ├── client
│   │   ├── main.py         # Entry point for the client application
│   │   ├── audio.py        # Functions for recording and playing audio messages
│   │   ├── chat.py         # Manages chat functionalities
│   │   └── call.py         # Handles voice call functionalities
│   ├── server
│   │   ├── main.py         # Entry point for the server application
│   │   ├── group.py        # Manages group chat functionalities
│   │   ├── message.py      # Handles message storage and retrieval
│   │   └── call.py         # Manages server-side call functionalities
│   ├── utils
│   │   ├── protocol.py     # Defines communication protocols
│   │   └── history.py      # Manages message history
│   └── types
│       └── __init__.py     # Defines types and interfaces
├── requirements.txt         # Lists project dependencies
└── README.md                # Documentation for the project
```

### Requirements

To run this application, you need to install the required dependencies. You can do this by running:

```
pip install -r requirements.txt
```

### Running the Application

1. Start the server by navigating to the `src/server` directory and running:

   ```
   python main.py
   ```
2. Start the client by navigating to the `src/client` directory and running:

   ```
   python main.py
   ```

### Contributors

- Nicolás Jimenez
- Juan Rosero
- Juan Ocampo
- Manuel Rojas
