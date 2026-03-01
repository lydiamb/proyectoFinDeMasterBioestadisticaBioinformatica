FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
COPY . .

# Damos permisos de ejecución al wrapper de Maven
RUN chmod +x mvnw
# Ahora sí, construimos
RUN ./mvnw clean package -DskipTests
# Construimos el archivo .jar (saltando los tests para ir rápido)
RUN ./mvnw clean package -DskipTests

FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]