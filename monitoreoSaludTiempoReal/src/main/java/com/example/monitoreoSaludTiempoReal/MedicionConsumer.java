package com.example.monitoreoSaludTiempoReal;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

import com.example.monitoreoSaludTiempoReal.entity.AlertaEntity;
import com.example.monitoreoSaludTiempoReal.repository.AlertaRepository;

@Service
public class MedicionConsumer {

	@Autowired
	private AlertaRepository repository;
	
	@KafkaListener(topics = "telemetria-medica", groupId = "grupo-hospital-benidorm")
	public void listen(Medicion medicion) {
	    if (medicion.frecuenciaCardiaca() > 100 || medicion.oxigeno() < 95) {
	        System.err.println("🚨 Guardando alerta completa para " + medicion.pacienteId());
	        // Pasamos frecuencia y oxigeno al constructor
	        repository.save(new AlertaEntity(
	            medicion.pacienteId(), 
	            medicion.frecuenciaCardiaca(), 
	            medicion.oxigeno()
	        ));
	    }
	}
}