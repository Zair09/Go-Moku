# Gomoku con Inteligencia Artificial (Minimax + Poda Alfa-Beta)

## Descripción

Implementación del juego de estrategia Gomoku (5 en línea) con una inteligencia artificial avanzada basada en el algoritmo Minimax con poda alfa-beta. El proyecto permite enfrentar diferentes tipos de agentes (IA, Greedy, Random, Humano) en un tablero de 15x15, donde el objetivo es formar una línea de 5 fichas consecutivas en cualquier dirección.

El sistema incluye un motor de búsqueda adversarial optimizado con búsqueda iterativa por profundidad, función heurística combinada para evaluar amenazas y bloqueos, y un sistema de benchmarking para medir el rendimiento del algoritmo.

## Objetivo

Este proyecto fue desarrollado para demostrar competencias en:
- **Algoritmos de búsqueda adversarial**: Implementación correcta de Minimax con poda alfa-beta
- **Diseño de heurísticas**: Creación de funciones de evaluación efectivas para juegos de estrategia
- **Optimización de rendimiento**: Reducción del espacio de búsqueda mediante poda inteligente de movimientos
- **Pensamiento algorítmico**: Análisis de complejidad temporal y trade-offs entre profundidad y tiempo
- **Resolución de problemas complejos**: Diseño de un agente inteligente capaz de competir en juegos de estrategia

## Tecnologías Utilizadas

- **Python 3.7+**: Lenguaje principal
- **NumPy**: Manejo de valores infinitos para alfa-beta y operaciones numéricas
- **Copy (módulo estándar)**: Deep copy de estados del juego para exploración del árbol
- **Time**: Gestión de límites de tiempo y búsqueda iterativa
- **Random**: Implementación de agente aleatorio para comparaciones

## Funcionalidades Principales

### Sistema de Juego
- **5 tipos de agentes disponibles**: Humano, IA (Minimax), Greedy, Random, Worst
- **Tablero configurable** de 15x15 con detección automática de victorias
- **Interfaz de consola** con visualización clara del estado del juego
- **Validación de movimientos** y manejo de errores de entrada

### Inteligencia Artificial
- **Minimax con poda alfa-beta**: Optimización que reduce nodos explorados de O(b^d) a O(b^(d/2))
- **Búsqueda iterativa por profundidad**: Aumenta profundidad progresivamente hasta agotar el tiempo límite
- **Detección de victorias/bloqueos inmediatos**: Prioriza movimientos críticos antes de explorar el árbol
- **Ordenamiento inteligente de movimientos**: Victoria > Bloqueo > Amenaza > Neutral para maximizar eficiencia de poda
- **Poda espacial de jugadas**: Solo explora casillas en radio de 2 posiciones de fichas existentes, reduciendo factor de ramificación de ~225 a ~20-40

### Función Heurística Combinada
```python
Evaluación = 
  + Victoria inmediata (10000)
  - Derrota inmediata (-10000)
  + Doble amenaza de 4 (9000)
  + Amenaza simple de 4 (1000)
  + Líneas de 3 (200 c/u)
  + Líneas de 2 (80 c/u)
  - Amenazas rivales de 4 (-5000)
  - Amenazas rivales de 3 (-500 c/u)
  + Control del centro (5 × distancia)
```

### Sistema de Benchmarking
- **Contador de nodos expandidos**: Mide eficiencia del algoritmo
- **Profundidad máxima alcanzada**: Indica capacidad de lookahead
- **Tiempo total de pensamiento**: Optimización de decisiones por segundo
- **Registro de resultados**: Ganador, puntaje final y métricas de rendimiento

## Aprendizajes Clave

### Algoritmos y Estructuras de Datos
- Implementación práctica de **búsqueda adversarial** en juegos de suma cero
- Comprensión profunda de **poda alfa-beta** y su impacto en performance (reducción ~60% de nodos)
- Diseño de **funciones heurísticas** balanceadas entre múltiples objetivos
- **Búsqueda iterativa**: Gestión de recursos computacionales con límites de tiempo (anytime algorithms)

### Optimización y Rendimiento
- **Trade-offs entre profundidad y anchura**: Decisiones de diseño en espacios de búsqueda grandes
- **Ordenamiento de movimientos**: Impacto crítico en eficiencia de poda (factor de mejora 2-5x)
- **Poda espacial**: Reducción del factor de ramificación mediante conocimiento del dominio
- **Análisis de complejidad**: Medición empírica de nodos expandidos vs profundidad

### Pensamiento Estratégico
- **Detección de patrones tácticos**: Amenazas múltiples, bloqueos obligatorios, control posicional
- **Evaluación de estados**: Cuantificación de ventajas posicionales en juegos abstractos
- **Anticipación de respuestas**: Modelado del comportamiento del oponente

### Ingeniería de Software
- **Separación de responsabilidades**: GameState, MinimaxSolver, funciones de evaluación independientes
- **Diseño modular**: Fácil experimentación con diferentes configuraciones y agentes
- **Deep copy de estados**: Exploración no destructiva del árbol de juego
- **Benchmarking sistemático**: Medición objetiva de rendimiento para comparar configuraciones

## Ejemplo / Demo

```
   1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
1  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
2  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
3  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
4  .  .  .  .  .  X  .  .  .  .  .  .  .  .  .
5  .  .  .  .  O  X  .  .  .  .  .  .  .  .  .
6  .  .  .  O  X  O  .  .  .  .  .  .  .  .  .
7  .  .  O  X  O  X  .  .  .  .  .  .  .  .  .
8  .  X  O  X  O  .  .  .  .  .  .  .  .  .  .
9  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .

Máquina pensando (X)...
La máquina pensó durante 2.34 segundos

Resumen del benchmark:
Ganador: X
Tiempo total pensando: 45.67 segundos
Nodos expandidos: 145,823
Profundidad alcanzada: 6
```

## Cómo Ejecutar el Proyecto

### Requisitos Previos
```bash
Python 3.7 o superior
numpy
```

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/Zair09/Go-Moku.git
cd GO-MOKU

# Instalar dependencias
pip install numpy
```

### Ejecución
```bash
python GoMoku_Pruebas.py
```

### Configuración Inicial
Al iniciar, selecciona el tipo de jugador para X y O:
```
Opciones: humano, ia, random, greedy, worst

Selecciona tipo de jugador para Jugador X: ia
Selecciona tipo de jugador para Jugador O: humano
```

### Jugar como Humano
- Ingresa coordenadas en formato: `x y` (ejemplo: `8 8`)
- Las coordenadas van de 1 a 15
- Objetivo: Formar 5 fichas consecutivas en línea

### Parámetros Configurables
```python
# En el código:
BOARD_SIZE = 15          # Tamaño del tablero
time_limit = 3           # Segundos por movimiento de IA
weights = [3]            # Pesos de heurística 
```

## Estado del Proyecto

**Proyecto académico finalizado** – Desarrollado para la materia de Inteligencia Artificial en ITLA.

### Características Completadas
    Motor de juego Gomoku completo con detección de victorias  
    Minimax con poda alfa-beta implementado correctamente  
    Búsqueda iterativa por profundidad con límite de tiempo  
    5 tipos de agentes (Humano, IA, Greedy, Random, Worst)  
    Función heurística combinada con evaluación de amenazas  
    Sistema de benchmarking completo  
    Optimizaciones de rendimiento (poda espacial, ordenamiento de movimientos)  

### Experimentos Realizados
- Comparación de diferentes configuraciones de pesos heurísticos
- Análisis de impacto del límite de tiempo (1s, 3s, 10s)
- Medición de nodos expandidos vs profundidad alcanzada
- Evaluación de eficiencia de poda alfa-beta

### Posibles Mejoras Futuras
- Implementar tabla de transposición para evitar recálculo de estados
- Agregar detección de patrones complejos (doble 3, 4 abierto)
- Interfaz gráfica con Pygame
- Monte Carlo Tree Search (MCTS) como alternativa a Minimax

## Autor

**Rony Zair Peguero Díaz**  
Estudiante de Desarrollo de Software – ITLA  
📧 ronizairp@gmail.com  
📍 Santo Domingo, República Dominicana

---