<<<<<<< HEAD
# 1. Usamos Maven con Java 21 para la compilación
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app

# 2. Copiamos el pom y descargamos dependencias
COPY pom.xml .
RUN mvn dependency:go-offline -B

# 3. Copiamos el código fuente y compilamos
COPY src ./src
RUN mvn clean package -DskipTests

# 4. Imagen final ligera con Java 21 (JRE)
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app

# 5. Copiamos el archivo .jar generado
COPY --from=build /app/target/*.jar app.jar

=======
# Paso 1: Usar una imagen de Java 25 (o la versión que estés usando)
FROM eclipse-temurin:21-jdk-jammy AS build
WORKDIR /app
COPY . .
# Construimos el archivo .jar (saltando los tests para ir rápido)
RUN ./mvnw clean package -DskipTests

# Paso 2: Imagen ligera para ejecutar
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
>>>>>>> e49bf05 (suida inicial de archivos del proyecto)
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]