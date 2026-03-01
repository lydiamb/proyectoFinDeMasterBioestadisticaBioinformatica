# Paso 1: Usar una imagen de Java 25 (o la versión que estés usando)
FROM eclipse-temurin:21-jdk-jammy AS build
WORKDIR /app
COPY . .

# Damos permisos de ejecución al wrapper de Maven
RUN chmod +x mvnw
# Ahora sí, construimos
RUN ./mvnw clean package -DskipTests
# Construimos el archivo .jar (saltando los tests para ir rápido)
RUN ./mvnw clean package -DskipTests

# Paso 2: Imagen ligera para ejecutar
FROM eclipse-temurin:21-jre-jammy
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]