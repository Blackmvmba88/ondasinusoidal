# 🎵 Ondasinusoidal - Visualización Esperada

## Cuando el programa está en ejecución

### Terminal (Consola)
```
═══════════════════════════════════════════════════════════
     🎵 Visualizador de Ondas Sinusoidales en Tiempo Real 🎵
═══════════════════════════════════════════════════════════

Iniciando captura de audio...
Presiona Ctrl+C para salir

╭────────────────────────────────────────────────────╮
│  🎼 Analizador de Audio en Tiempo Real 🎼           │
├────────────────────────────────────────────────────┤
│                                                    │
│  🎵 Frecuencia:    440.2 Hz                        │
│  📊 Amplitud:      0.7854                          │
│  🔊 Nivel:         -12.3 dB                        │
│  📈 Visual:        ████████████████░░░░            │
│                                                    │
╰────────────────────────────────────────────────────╯

(Los valores se actualizan 10 veces por segundo)
(El color del borde cambia según la frecuencia)
```

### Ventana Matplotlib (Gráficos)

```
┌──────────────────────────────────────────────────────────────┐
│                  Forma de Onda Sinusoidal                    │
│                                                              │
│  1.0 ┤                                                       │
│      │    ╱╲        ╱╲        ╱╲        ╱╲                 │
│  0.5 ┤   ╱  ╲      ╱  ╲      ╱  ╲      ╱  ╲                │
│      │  ╱    ╲    ╱    ╲    ╱    ╲    ╱    ╲               │
│  0.0 ┤─╱──────╲──╱──────╲──╱──────╲──╱──────╲─             │
│      │         ╲╱        ╲╱        ╲╱        ╲╱             │
│ -0.5 ┤                                                       │
│      │                                                       │
│ -1.0 ┤                                                       │
│      └─────────┬─────────┬─────────┬─────────┬─────         │
│               500      1000      1500      2000              │
│                    Tiempo (muestras)                         │
├──────────────────────────────────────────────────────────────┤
│                  Espectro de Frecuencias                     │
│                                                              │
│  1.0 ┤                                                       │
│      │                                                       │
│  0.8 ┤    ▂▃                                                 │
│      │   ▅███▅                                               │
│  0.6 ┤  ███████▄                                             │
│      │ ██████████▄▂                                          │
│  0.4 ┤████████████████▅▃▂▁▁                                 │
│      │████████████████████████▅▄▃▂▂▁▁▁                      │
│  0.2 ┤██████████████████████████████████▅▄▃▂▂▁▁             │
│      │                                                       │
│  0.0 ┤────────────────────────────────────────────           │
│      └────┬────┬────┬────┬────┬────┬────┬────┬──            │
│         1000  2000  3000  4000  5000  6000  7000            │
│                    Frecuencia (Hz)                           │
└──────────────────────────────────────────────────────────────┘

Colores:
- El color de las líneas cambia dinámicamente según la frecuencia
- Paleta psicodélica: Magenta, Cyan, Amarillo, Rosa, Verde, Violeta
- Fondo oscuro (#0a0a0a) con grillas sutiles
- Los colores rotan según: color_idx = (frecuencia / 100) % 6
```

## Comportamiento Dinámico

### Cuando hay silencio:
- Frecuencia: ~0 Hz
- Amplitud: ~0.0000
- Nivel: -60 dB (mínimo)
- Onda: Línea casi recta
- Espectro: Plano, sin picos

### Cuando se habla/canta (ejemplo: nota La 440Hz):
- Frecuencia: ~440 Hz (nota musical La)
- Amplitud: 0.3 - 0.8 (según volumen)
- Nivel: -30 a -10 dB
- Onda: Sinusoide clara y definida
- Espectro: Pico prominente en 440 Hz + armónicos
- Color: Amarillo (#FFFF00)

### Cuando hay música compleja:
- Frecuencia: Varía constantemente (50-5000 Hz)
- Amplitud: 0.5 - 1.0
- Nivel: -20 a 0 dB
- Onda: Forma compleja con múltiples frecuencias
- Espectro: Múltiples picos distribuidos
- Color: Cambia rápidamente creando efecto psicodélico

### Cuando hay ruido/percusión:
- Frecuencia: Errática (todo el espectro)
- Amplitud: Variable, picos súbitos
- Nivel: Fluctúa rápidamente
- Onda: Irregular, caótica
- Espectro: Distribución amplia sin picos definidos
- Color: Cambios rápidos y aleatorios

## Interacciones

### Inicio del programa:
1. Muestra banner de bienvenida en terminal
2. Inicializa captura de audio (puede pedir permisos de micrófono)
3. Abre ventana de matplotlib con gráficos vacíos
4. Comienza actualización en tiempo real

### Durante ejecución:
- Terminal: Actualiza estadísticas 10 veces/segundo
- Gráficos: Se actualizan 20 veces/segundo (20 FPS)
- Respuesta inmediata al sonido (<50ms de latencia)
- Colores cambian suavemente según frecuencia
- Los hilos trabajan en paralelo sin bloqueos

### Salida del programa:
- Ctrl+C en terminal o cerrar ventana matplotlib
- Mensaje: "Cerrando visualizador..."
- Limpieza de recursos (stream de audio, hilos)
- Mensaje final: "¡Hasta luego!"

## Requerimientos de Hardware

- **Micrófono**: Cualquier dispositivo de entrada de audio
- **CPU**: ~5-10% de uso en procesador moderno
- **RAM**: ~50-100 MB
- **GPU**: No requerida (todo renderizado por CPU)
- **Pantalla**: Resolución mínima 1024x768 para ventana matplotlib

## Prueba Rápida

Para probar el programa sin micrófono real, se puede:
1. Usar entrada de audio virtual/loopback
2. Reproducir audio y capturarlo con el sistema
3. Ejecutar test_ondasinusoidal.py para validar la lógica

## Notas

- Los colores psicodélicos crean un efecto visual hipnótico
- La combinación de terminal + gráficos proporciona análisis completo
- Ideal para educación, música, arte generativo, y debugging de audio
- Código abierto y totalmente personalizable
