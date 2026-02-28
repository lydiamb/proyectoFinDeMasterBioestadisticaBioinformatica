package com.example.monitoreoSaludTiempoReal.controller;

import com.example.monitoreoSaludTiempoReal.repository.AlertaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebController {

    @Autowired
    private AlertaRepository alertaRepository;

    @GetMapping("/dashboard")
    public String verDashboard(Model model) {
        // Pasamos la lista de alertas a la web
        model.addAttribute("alertas", alertaRepository.findAll());
        return "dashboard"; // Esto buscará el archivo dashboard.html
    }
}