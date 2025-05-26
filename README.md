# Chat_MC - Aplicación de Chat

## Descripción

Este proyecto es una aplicación de chat que permite la comunicación entre múltiples clientes mediante mensajes de texto, notas de voz y llamadas de voz. Además, guarda el historial de mensajes enviados.
---
## Integrantes

- Nicolás Jimenez
- Juan Rosero
- Juan Ocampo
- Manuel Rojas

---

### Requerimientos

- Crear grupos de chat.
- Enviar mensajes de texto a un usuario específico o a un grupo.
- Enviar notas de voz a un usuario específico o a un grupo.
- Realizar llamadas a un usuario o a un grupo.
- Guardar el historial de mensajes enviados (texto y audios).

Para cada requerimiento se debe escoger el protocolo de comunicación (TCP o UDP) más apropiado. La interacción puede realizarse por línea de comandos o mediante una interfaz gráfica.

**Entrega:**  
Además del código fuente, se debe entregar este README con las instrucciones para ejecutar el programa y los nombres de los integrantes.
### Instrucciones para Windows

1. **Requisitos previos**
   - Tener instalado **Java JDK 8 o superior**.
   - Usar el símbolo del sistema (cmd) o PowerShell.

2. **Compilar el proyecto**

   Abre el símbolo del sistema y navega a la carpeta del proyecto:

   ```bat
   cd ruta\al\proyecto\Chat_MC\ChatLlamadas\src
   ```

   Luego ejecuta:

   ```bat
   javac *.java
   ```

3. **Iniciar el servidor**

   En la misma carpeta (`src`), ejecuta:

   ```bat
   java Servidor
   ```

4. **Iniciar un cliente**

   Abre otra ventana del símbolo del sistema, navega a la misma carpeta (`src`) y ejecuta:

   ```bat
   java Cliente
   ```

   Sigue las instrucciones en pantalla para ingresar tu nickname y unirte o crear un chat.

5. **Notas adicionales**
   - Puedes abrir varias ventanas y ejecutar varios clientes para simular múltiples usuarios.
   - Los mensajes y audios se guardan automáticamente en la carpeta `src\data\` bajo el nombre del chat.
   - Para salir de la aplicación, selecciona la opción correspondiente en el menú del cliente.

---

## Instrucciones para linux

### 1. Requisitos previos

- **Java JDK 8 o superior** instalado.
- Sistema operativo Linux (probado en Linux).
- Terminal de comandos.

### 2. Compilar el proyecto

Abre una terminal en la carpeta raíz del proyecto (`Chat_MC/ChatLlamadas/src`) y ejecuta:

```sh
javac *.java
```

Esto compilará todos los archivos `.java` necesarios.

### 3. Iniciar el servidor

En la misma carpeta (`src`), ejecuta:

```sh
java Servidor
```

Verás un mensaje indicando que el servidor está iniciado.

### 4. Iniciar un cliente

Abre otra terminal, navega a la misma carpeta (`src`) y ejecuta:

```sh
java Cliente
```

Sigue las instrucciones en pantalla para ingresar tu nickname y unirte o crear un chat.

### 5. Notas adicionales

- Puedes abrir varias terminales y ejecutar varios clientes para simular múltiples usuarios.
- Los mensajes y audios se guardan automáticamente en la carpeta `src/data/` bajo el nombre del chat.
- Para salir de la aplicación, selecciona la opción correspondiente en el menú del cliente.

