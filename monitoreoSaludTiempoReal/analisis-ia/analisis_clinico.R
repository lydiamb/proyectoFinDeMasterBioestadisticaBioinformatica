# analisis_clinico.R
library(ggplot2)
library(gridExtra) # Para organizar tablas y gráficos en el mismo PDF
library(grid)

# 1. Leer datos y metadatos
datos <- read.csv("datos_para_r.csv")
fecha_hora <- format(Sys.time(), "%d/%m/%Y %H:%M:%S")

# 2. Calcular Estadísticos (El "Summary" para el médico)
calc_stats <- function(x) {
  c(Media = mean(x, na.rm=T), 
    Desv.Std = sd(x, na.rm=T), 
    Varianza = var(x, na.rm=T),
    Min = min(x, na.rm=T), 
    Max = max(x, na.rm=T))
}

stats_frecuencia <- calc_stats(datos$frecuencia)
stats_oxigeno <- calc_stats(datos$oxigeno)

tabla_stats <- data.frame(
  Metrica = c("Frecuencia (BPM)", "Oxigeno (%)"),
  rbind(stats_frecuencia, stats_oxigeno)
)

# 3. Crear el Gráfico (Boxplot + Puntos)
df_stack <- stack(datos[, c("frecuencia", "oxigeno")])
p <- ggplot(df_stack, aes(x=ind, y=values, fill=ind)) +
  geom_boxplot(alpha=0.6) +
  geom_jitter(width=0.2, alpha=0.4) +
  labs(title="Distribución de Constantes Vitales", x="", y="Valor") +
  theme_minimal() +
  scale_fill_manual(values=c("#ff4b4b", "#3498db")) +
  theme(legend.position="none")

# 4. Generar el PDF con texto y tabla
pdf("informe_estadistico.pdf", width=8.5, height=11)

# Título y Cabecera
# --- VERSIÓN CORREGIDA DEL MAQUETADO ---

grid.reorder <- function() {
  grid.newpage()
  
  # 1. Título y Cabecera (Parte Superior)
  grid.text("HOSPITAL IA – REPORTE CLÍNICO DIARIO", y=unit(0.95, "npc"), gp=gpar(fontsize=18, fontface="bold"))
  grid.text(paste("Fecha de generación:", fecha_hora), y=unit(0.91, "npc"), gp=gpar(fontsize=10))
  grid.text(paste("Total de registros analizados:", nrow(datos)), y=unit(0.89, "npc"), gp=gpar(fontsize=10))
  
  # 2. Título de la Tabla
  grid.text("1. Resumen Estadístico de la Sesión", y=unit(0.84, "npc"), x=unit(0.5, "npc"), gp=gpar(fontface="bold", fontsize=12))
  
  # 3. Dibujar la Tabla (Posicionada en la mitad superior)
  pushViewport(viewport(y=unit(0.72, "npc"), height=unit(0.2, "npc")))
  grid.table(tabla_stats)
  popViewport()
  
  # 4. Título del Gráfico
  grid.text("2. Análisis Visual de Distribución", y=unit(0.58, "npc"), x=unit(0.5, "npc"), gp=gpar(fontface="bold", fontsize=12))
  
  # 5. Dibujar el Gráfico (Posicionado en la mitad inferior, dándole más espacio)
  # El parámetro 'y' define el centro del gráfico, bajándolo para que no pise la tabla
  pushViewport(viewport(y=unit(0.32, "npc"), height=unit(0.45, "npc")))
  print(p, newpage = FALSE) 
  popViewport()
  
  # Pie de página
  grid.text("Firma del Sistema de IA: Verificado", y=unit(0.05, "npc"), gp=gpar(fontsize=8, fontitalic=T, col="grey"))

}

grid.reorder()
dev.off()

cat("✅ Informe médico completo generado\n")