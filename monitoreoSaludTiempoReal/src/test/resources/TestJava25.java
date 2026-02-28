import java.time.Duration;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

public class TestJava25 {
    public static void main(String[] args) {
        System.out.println("🚀 Iniciando prueba con Hilos Virtuales...");

        long inicio = System.currentTimeMillis();

        // Usamos un Executor que crea un hilo virtual por cada tarea
        try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
            IntStream.range(0, 10_000).forEach(i -> {
                executor.submit(() -> {
                    // Simulamos una tarea que tarda un poco (ej. una consulta a base de datos)
                    Thread.sleep(Duration.ofSeconds(1));
                    if (i % 1000 == 0) {
                        System.out.println("✅ Tarea " + i + " completada por: " + Thread.currentThread());
                    }
                    return i;
                });
            });
        } // El try-with-resources cierra el executor y espera a que todos terminen

        long fin = System.currentTimeMillis();
        
        System.out.println("---");
        System.out.println("⏱️ Tiempo total para 10,000 tareas: " + (fin - inicio) + " ms");
        System.out.println("💡 Nota: ¡Solo ha tardado poco más de 1 segundo en procesar 10,000 esperas!");
    }
}