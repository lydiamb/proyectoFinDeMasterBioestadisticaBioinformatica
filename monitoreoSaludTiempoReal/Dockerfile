# 1. Usamos una imagen que YA tiene Maven instalado
FROM maven:3.9-eclipse-temurin-17 AS build

# 2. Directorio de trabajo
WORKDIR /app

# 3. Copiamos el archivo de configuración de dependencias primero (Optimiza el build)
COPY pom.xml .

# 4. Copiamos todo el código fuente
COPY src ./src

# 5. CONSTRUIMOS usando 'mvn' directamente (sin el ./mvnw)
# Esto ignora el archivo rebelde y usa el Maven del sistema
RUN mvn clean package -DskipTests

# 6. Imagen ligera final
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]