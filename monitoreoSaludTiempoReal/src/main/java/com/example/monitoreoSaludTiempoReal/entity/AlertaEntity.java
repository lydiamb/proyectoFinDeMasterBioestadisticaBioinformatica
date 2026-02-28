package com.example.monitoreoSaludTiempoReal.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class AlertaEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String pacienteId;
    private int frecuencia;
    private int oxigeno;
    private LocalDateTime fecha = LocalDateTime.now();

    // Constructores, Getters y Setters (o usa Lombok si sabes)
    public AlertaEntity() {}
    public AlertaEntity(String pacienteId, int frecuencia, int oxigeno) {
        this.pacienteId = pacienteId;
        this.frecuencia = frecuencia;
        this.oxigeno = oxigeno;
    }
    public String getPacienteId() { return pacienteId; }
    public int getFrecuencia() { return frecuencia; }
    public int getOxigeno() { return oxigeno; }
    public Long getId() {
        return id;
    }
}