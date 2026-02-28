package com.example.monitoreoSaludTiempoReal;

import org.springframework.boot.CommandLineRunner;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Component;
import java.util.Random;

@Component
public class SimuladorMediciones implements CommandLineRunner {

    private final KafkaTemplate<String, Medicion> kafkaTemplate;

    public SimuladorMediciones(KafkaTemplate<String, Medicion> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @Override
    public void run(String... args) throws Exception {
        // Un pequeño delay para esperar a que el Consumer esté listo
    	System.out.println("⏳ Esperando 10 segundos a que Kafka esté listo...");
        Thread.sleep(10000); // <--- Espera 10 segundos
        
        Random random = new Random();

        for (int i = 1; i <= 50; i++) {
            String id = "PAC-00" + i;
            // Generamos ritmo entre 60 y 130
            int ritmo = 60 + random.nextInt(71); 
            int oxigeno = 94 + random.nextInt(6);

            Medicion m = new Medicion(id, ritmo, oxigeno);
            
            System.out.println("📤 Enviando: " + m.pacienteId() + " (Ritmo: " + ritmo + ")");
            kafkaTemplate.send("telemetria-medica", m);
            
            Thread.sleep(1000); // Un pequeño respiro entre envíos
        }
        System.out.println("✅ Fin de la simulación.");
    }
}