package com.example.monitoreoSaludTiempoReal.controller;

import org.springframework.web.bind.annotation.*;

import com.example.monitoreoSaludTiempoReal.entity.AlertaEntity;
import com.example.monitoreoSaludTiempoReal.entity.ConclusionIA;
import com.example.monitoreoSaludTiempoReal.repository.AlertaRepository;

import java.util.List;

@RestController
@RequestMapping("/alertas")
public class AlertaController {

    private final AlertaRepository repository;

    // Inyectamos el repositorio para poder consultar la base de datos
    public AlertaController(AlertaRepository repository) {
        this.repository = repository;
    }

    // GET http://localhost:8080/alertas
    // Este es el que usa Python para descargar los datos y analizarlos
    @GetMapping
    public List<AlertaEntity> obtenerTodas() {
        return repository.findAll();
    }

    // POST http://localhost:8080/alertas/conclusion
    // Este es el que usa Python para enviarnos sus descubrimientos
    @PostMapping("/conclusion")
    public void recibirConclusion(@RequestBody ConclusionIA conclusion) {
        System.out.println("\n--- 🤖 REPORTE RECIBIDO DE LA IA ---");
        System.out.println("🆔 Alerta Referencia: " + conclusion.alertaId());
        System.out.println("📝 Diagnóstico Experto: " + conclusion.diagnostico());
        System.out.println("⚠️ Nivel de Riesgo: " + conclusion.nivelRiesgo());
        System.out.println("------------------------------------\n");
        
        // Aquí es donde en un sistema real se dispararía la lógica de emergencia
    }
    
    
}