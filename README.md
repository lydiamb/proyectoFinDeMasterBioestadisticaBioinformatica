# 🏥 Sistema Inteligente de Monitoreo Médico (IA-Health)

Este proyecto es una plataforma de telemetría médica en tiempo real que utiliza una arquitectura políglota basada en microservicios. 

Combina la potencia de **Java 21** para la infraestructura, **Apache Kafka** para el flujo de datos, **Python** para el análisis predictivo con IA y **R** para el rigor bioestadístico.

---

## 🚀 <u>Requisito Único:</u> Docker Desktop

Para garantizar que el sistema funcione exactamente igual en cualquier ordenador, el proyecto está completamente contenedorizado. El único software que necesitas tener instalado es **Docker Desktop** (disponible para Windows, Mac y Linux).

* **Descargar Docker Desktop aquí:** [Microsoft Store / Oficial](https://apps.microsoft.com/detail/xp8cbj40xlbwkx?hl=es-ES&gl=SO)

> **Nota importante:** No es necesario instalar Java, Python o R por separado en tu máquina local, ya que Docker se encarga de configurar estos entornos automáticamente dentro de los contenedores.

---

## 🛠️ Instrucciones de Instalación

Sigue estos pasos para poner en marcha todo el ecosistema:

1. **Clonar el repositorio:**

	 git clone [https://github.com/lydiamb/proyectoFinDeMasterBioestadisticaBioinformatica.git](https://github.com/lydiamb/proyectoFinDeMasterBioestadisticaBioinformatica.git)
	 cd proyectoFinDeMasterBioestadisticaBioinformatica
   
2. **Levantar el sistema con Docker:**

	Abre una terminal en la carpeta raíz del proyecto y ejecuta:
	
	<i>docker-compose up --build</i>
	
	Este comando descargará las imágenes necesarias, compilará el backend de Java y configurará los entornos de Python y R. Puede tardar unos minutos la primera vez.
	
	Acceder a las plataformas:
	Una vez que los contenedores estén activos (en verde) en Docker Desktop:
	
	Dashboard IA (Python + R): http://localhost:8501
	
	API de Control (Java): http://localhost:8080/alertas

## 🏗️ Arquitectura del Proyecto

El sistema se divide en cuatro módulos principales que trabajan en armonía:

<table>
<thead>
<tr>
<th>Módulo</th>
<th>Tecnología</th>
<th>Función</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>Backend</b></td>
<td>Java 21 / Spring Boot</td>
<td>Orquestación de datos y API REST.</td>
</tr>
<tr>
<td><b>Mensajería</b></td>
<td>Apache Kafka</td>
<td>Transmisión de constantes vitales en tiempo real.</td>
</tr>
<tr>
<td><b>Análisis IA</b></td>
<td>Python / Streamlit</td>
<td>Dashboard visual y predicción de tendencias cardíacas.</td>
</tr>
<tr>
<td><b>Bioestadística</b></td>
<td>R Language</td>
<td>Generación de informes clínicos en PDF con QR integrado.</td>
</tr>
</tbody>
</table>


## 📊 Funcionalidades Destacadas

* Detección de Anomalías: Identificación automática de derivas peligrosas en el ritmo cardíaco.

* Analítica Predictiva: Uso de regresión lineal para anticipar el estado del paciente en los próximos 60 segundos.

* Reportes Clínicos: Botón integrado para generar un análisis Bioestadístico en PDF mediante el motor de R.

* Acceso Digital QR: Cada informe incluye un código QR que permite al médico volver al panel en tiempo real desde cualquier dispositivo móvil.

## 📝 Autor

Lydia Manzanares - Proyecto de Fin de Máster Bioinformática y bioestadística - 2026
