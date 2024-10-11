package org.example;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;

public class BLEFirmataControl {
    public static void main(String[] args) {
        try {
            // Run the Python script that communicates via Bluetooth
            ProcessBuilder processBuilder = new ProcessBuilder("python", "src/main/python/ble_firmata_control.py");
            Process process = processBuilder.start();

            // Set up readers for the script's output and input
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            PrintWriter writer = new PrintWriter(new OutputStreamWriter(process.getOutputStream()), true);

            // Communicate with the Python script
            String line;
            boolean readyToProceed = false;

            while ((line = reader.readLine()) != null) {
                System.out.println("Python says: " + line);

                if (line.contains("Connected to Arduino")) {
                    readyToProceed = true;
                    System.out.println("Connection established with Arduino. Ready to send commands...");
                }

                // Send command to Python only if ready
                if (readyToProceed) {
                    writer.println("BLINK");
                    Thread.sleep(1000); // Keep sending the BLINK command every second
                }
            }

            // Close the streams
            reader.close();
            writer.close();
            process.waitFor();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
