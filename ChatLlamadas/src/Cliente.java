import java.io.*;
import java.net.*;
import java.util.Arrays;
import java.util.Scanner;

import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;

public class Cliente {
    private Socket socket;
    private Socket audioSocket;
    private BufferedReader in;
    private PrintWriter out;
    private DataInputStream dis;
    private DataOutputStream dos;
    private String nickname;
    private Thread listenerThread;
    private Thread audioListenerThread;
    private String currentChatName;

    private volatile boolean onCall = false;
    private volatile int callPort = 0;

    private static final int SAMPLE_RATE = 16000;
    private static final int SAMPLE_SIZE_IN_BITS = 16;
    private static final int CHANNELS = 1;
    private static final boolean SIGNED = true;
    private static final boolean BIG_ENDIAN = true;
    private static final AudioFormat format = new AudioFormat(SAMPLE_RATE, SAMPLE_SIZE_IN_BITS, CHANNELS, SIGNED, BIG_ENDIAN);

    public Cliente(String address, int port, int audioPort, String nickname) {
        try {
            this.nickname = nickname;
            this.socket = new Socket(address, port);
            this.audioSocket = new Socket(address, audioPort);
            this.in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            this.out = new PrintWriter(socket.getOutputStream(), true);
            this.dis = new DataInputStream(audioSocket.getInputStream());
            this.dos = new DataOutputStream(audioSocket.getOutputStream());

            // Enviar el nickname al servidor
            out.println(nickname);
            
            Scanner scanner = new Scanner(System.in);
            String opcion;
            // Solicitar el nombre del chat
            do{
                System.out.println("Menu:");
                System.out.println("1. Crear chat o unirse a chat");
                System.out.println("2. Ver chats disponibles");
                System.out.println("3. Salir");
                System.out.print("Elige una opción: ");
                opcion = scanner.nextLine();

                iniciarListener();

            if(opcion.equals("1")){
                out.println("chat");
                ingresarChat();
                
                // Iniciar hilo para escuchar mensajes
                iniciarAudioListener();
                // Permitir que el cliente envíe mensajes
                enviarMensajes();

            }else if(opcion.equals("2")){
                out.println("ver_chats");
            }else if (opcion.equals("3")){
                out.println("/exit");
                detenerListener();
                detenerAudioListener();
                break;
            }
            else{
                System.out.println("Opción no válida");


            }} while (!opcion.equals("3"));
            

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void ingresarChat() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Ingrese el nombre del chat para crear o unirse:");
        String chatName = scanner.nextLine();
        currentChatName = chatName;  // Guardar el nombre del chat actual
        out.println("/chat " + chatName);  // Enviar el nombre del chat al servidor
    }

    private void enviarMensajes() {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            String message = scanner.nextLine();
            if (!message.isEmpty()) {
                out.println(message);
                if(message.equals("/exit")){
                    break;
                }else if (message.startsWith("/call")) {
                onCall = true;
                startGroupCall(currentChatName);
                }else if (message.startsWith("/leave_call")) {
                    onCall = false;
                    out.println("/leave_call " + currentChatName + " " + callPort);
                }else if(!onCall){
                    if(message.equals("/audio")){
                    enviarAudio();  
                    }
                }
            }
        }
    }

    private void enviarAudio() {
        int duration = 5; // seconds
        ByteArrayOutputStream outAudio = new ByteArrayOutputStream();
        AudioRecorder recorder = new AudioRecorder(format, duration, outAudio);
        Thread t = new Thread(recorder);
        t.start();
        try {
            t.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        byte[] audio = outAudio.toByteArray();
        try {
            dos.writeInt(audio.length);
            dos.flush();
            dos.write(audio);
            dos.flush();
            System.out.println("Enviando audio...");
        } catch (IOException e) {
            e.printStackTrace();
        }

    }


    private void iniciarAudioListener() {
        detenerAudioListener();
        audioListenerThread = new Thread(new audioListener());
        audioListenerThread.start();
    }

    // Método para detener el audio listener
    private void detenerAudioListener() {
        if (audioListenerThread != null && audioListenerThread.isAlive()) {
            audioListenerThread.interrupt(); // Interrumpir el hilo de manera controlada
            audioListenerThread = null;
        }
    }

    // Método para iniciar el listener
    private void iniciarListener() {
        detenerListener();
        listenerThread = new Thread(new Listener());
        listenerThread.start();
    }

    // Método para detener el listener
    private void detenerListener() {
        if (listenerThread != null && listenerThread.isAlive()) {
            listenerThread.interrupt(); // Interrumpir el hilo de manera controlada
            listenerThread = null;
        }
    }

    private class Listener implements Runnable {
        public void run() {
            byte[] audioData;
            String serverMessage;
            try {
                while (!Thread.currentThread().isInterrupted() && (serverMessage = in.readLine()) != null ) {
                    System.out.println(serverMessage);
                }
            } catch (IOException e) {
                if (Thread.currentThread().isInterrupted()) {
                    System.out.println("Listener detenido.");
                } else {
                    e.printStackTrace();
                }
            }
        }
    }

    private class audioListener implements Runnable {
        public void run() {
            byte[] audioData;
            try {
                DataInputStream dataIn = new DataInputStream(audioSocket.getInputStream());
                while (!Thread.currentThread().isInterrupted()) {
                    int audioLength = dataIn.readInt();
                
                // Crear un buffer para el audio recibido
                audioData = new byte[audioLength];
                
                // Leer el audio en el buffer
                dataIn.readFully(audioData);  // Lee exactamente 'audioLength' bytes
                
                // Reproducir el audio recibido
                AudioPlayer player = new AudioPlayer(format);
                player.initAudio(audioData);  // Pasar los datos de audio al reproductor
            }} catch (IOException e) {
                if (Thread.currentThread().isInterrupted()) {
                    System.out.println("Listener detenido.");
                } else {
                    e.printStackTrace();
                }
            }
        }
    }

   private void startGroupCall(String chatName) {
    try {
        DatagramSocket udpSocket = new DatagramSocket(); 
        udpSocket.setTrafficClass(0x10); 

        int localPort = udpSocket.getLocalPort(); 
        callPort = localPort;
        out.println("/join_call " + chatName + " " + localPort); 

        Thread receiveThread = new Thread(() -> {
            byte[] buffer = new byte[4096]; 
            try {
                while (onCall) {
                    DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
                    udpSocket.receive(packet);
                    byte[] data = Arrays.copyOf(packet.getData(), packet.getLength());
                    new AudioPlayer(format).initAudio(data);
                }
            } catch (IOException e) {
                if (onCall) e.printStackTrace();
            }
        });
        receiveThread.setPriority(Thread.MAX_PRIORITY); 
        receiveThread.start();

        Thread.sleep(100); 

        
        Thread micThread = new Thread(() -> {
            try {
                TargetDataLine mic = AudioSystem.getTargetDataLine(Cliente.format);
                mic.open(Cliente.format);
                mic.start();

                byte[] buffer = new byte[4096]; // Match receive size
                InetAddress serverAddress = InetAddress.getByName("localhost");

                while (onCall) {
                    int read = mic.read(buffer, 0, buffer.length);
                    DatagramPacket packet = new DatagramPacket(buffer, read, serverAddress, 55555);
                    udpSocket.send(packet);
                }

                mic.stop();
                mic.close();
                udpSocket.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        micThread.setPriority(Thread.MAX_PRIORITY); 
        micThread.start();

    } catch (IOException | InterruptedException e) {
        e.printStackTrace();
    }
}

    

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingresa tu nickname: ");
        String nickname = scanner.nextLine();
        new Cliente("localhost", 12345, 12346, nickname);
    }
}
