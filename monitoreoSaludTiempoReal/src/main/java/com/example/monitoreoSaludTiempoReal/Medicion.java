package com.example.monitoreoSaludTiempoReal;

//Importante: Los Records de Java 17/25 son perfectos para esto
public record Medicion(
 String pacienteId, 
 int frecuenciaCardiaca, 
 int oxigeno
) {}