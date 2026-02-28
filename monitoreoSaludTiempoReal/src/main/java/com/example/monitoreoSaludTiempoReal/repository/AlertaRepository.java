package com.example.monitoreoSaludTiempoReal.repository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.example.monitoreoSaludTiempoReal.entity.AlertaEntity;

@Repository
public interface AlertaRepository extends JpaRepository<AlertaEntity, Long> {}