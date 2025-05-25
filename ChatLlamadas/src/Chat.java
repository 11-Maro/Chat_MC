import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.sound.sampled.AudioFileFormat;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;


public class Chat {
    private String name;
    private List<ClientHandler> clients;
    private Map<String, Integer> audioCounter;
    private String filePath;
    private File file;
    private String parentDirectory;

    public Chat(String name) {
        this.name = name;
        this.clients = new ArrayList<>();
        this.parentDirectory = "data/"+name;
        File parentDir = new File(parentDirectory);
        if (!parentDir.exists()) {
            parentDir.mkdirs(); // Crear el directorio si no existe
            File audioDir = new File(parentDirectory + "/audio");
            audioDir.mkdirs(); // Crear el subdirectorio de audio
        }

        this.filePath = parentDirectory +"/"+ name + ".txt";
        this.file = new File(filePath);
        this.audioCounter = new HashMap<>();
    }

    public synchronized void addClient(ClientHandler client) {
        clients.add(client);
        broadcast(client.getNickname() + " se ha unido al chat", null);
    }
    
    public synchronized void removeClient(ClientHandler client) {
        clients.remove(client);
        broadcast(client.getNickname() + " ha salido del chat", null);
    }
    
    public synchronized void broadcast(String message, ClientHandler sender) {
        try {
            writeData(message);
        } catch (IOException e) {
            e.printStackTrace();
        }
        for (ClientHandler client : clients) {
            if (client != sender) {  // No enviamos el mensaje al remitente
                client.sendMessage(message);
            }
        }
    }

    public synchronized void broadcastAudio(byte[] audioData, ClientHandler sender) {
        saveAudioToFile(audioData, sender.getNickname());
        for (ClientHandler client : clients) {
            if (client != sender) {  // No enviamos el audio al remitente
                    client.sendAudio(audioData);
            }
        }
    }

    public synchronized void writeData(String message) throws IOException{
        BufferedWriter escritor = new BufferedWriter(new FileWriter(file,true));
            escritor.write("\n"+message);
            escritor.flush();
            escritor.close();
    }

    public void saveAudioToFile(byte[] audioData, String senderNickname) {
    try {
        // Count audios per sender
        int count = audioCounter.getOrDefault(senderNickname, 0);
        audioCounter.put(senderNickname, count + 1);

        // Prepare directory
        File dir = new File(parentDirectory+"/audio/" + senderNickname);
        if (!dir.exists()) dir.mkdirs();

        // Build file path
        File wavFile = new File(dir, senderNickname + "_audio_" + count + ".wav");

        // Save the audio
        AudioFormat format = new AudioFormat(16000, 16, 1, true, true);
        ByteArrayInputStream bais = new ByteArrayInputStream(audioData);
        AudioInputStream ais = new AudioInputStream(bais, format, audioData.length / format.getFrameSize());

        AudioSystem.write(ais, AudioFileFormat.Type.WAVE, wavFile);
        ais.close();

        System.out.println(" Audio guardado: " + wavFile.getAbsolutePath());

    } catch (Exception e) {
        System.err.println("Error al guardar audio de " + senderNickname);
        e.printStackTrace();
    }
}


    
}
