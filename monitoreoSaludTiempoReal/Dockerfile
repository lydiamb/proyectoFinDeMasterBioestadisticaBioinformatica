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

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]