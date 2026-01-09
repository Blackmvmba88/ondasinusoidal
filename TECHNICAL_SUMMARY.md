# 🎵 Visualizador de Ondas Sinusoidales - Resumen Técnico

## Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                      ONDASINUSOIDAL                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐      ┌──────────────┐     ┌───────────┐ │
│  │  Micrófono   │ ───> │   PyAudio    │ ──> │   Buffer  │ │
│  └──────────────┘      └──────────────┘     └─────┬─────┘ │
│                                                    │        │
│                                           ┌────────▼──────┐ │
│                                           │ AudioProcessor│ │
│                                           │   (numpy +    │ │
│                                           │    scipy)     │ │
│                                           └───────┬───────┘ │
│                                                   │         │
│                              ┌────────────────────┴─────┐   │
│                              │                          │   │
│                    ┌─────────▼──────┐         ┌────────▼───┐│
│                    │  stats_queue   │         │ audio_queue││
│                    │   (viz/rich)   │         └────────┬───┘│
│                    └────┬─────┬─────┘                  │    │
│                         │     │                        │    │
│              ┌──────────▼─┐ ┌─▼────────────┐  ┌───────▼──┐ │
│              │   Rich     │ │  Matplotlib  │  │ Matplotlib││
│              │  Terminal  │ │  Visualizer  │  │   FFT     ││
│              │  Display   │ │  (Waveform)  │  │ Spectrum  ││
│              └────────────┘ └──────────────┘  └───────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Características Principales

### 1. Captura de Audio en Tiempo Real
- **Frecuencia de muestreo**: 44,100 Hz (calidad CD)
- **Resolución**: 16-bit
- **Canales**: Mono
- **Tamaño de buffer**: 2048 muestras (~46ms)

### 2. Procesamiento de Señal

#### Análisis FFT (Transformada Rápida de Fourier)
```python
# Ventana de Hanning para reducir efectos de borde
windowed = audio_data * np.hanning(len(audio_data))

# FFT para obtener espectro de frecuencias
fft_vals = fft(windowed)
fft_freq = fftfreq(len(windowed), 1.0/RATE)

# Encontrar frecuencia dominante
peak_idx = np.argmax(fft_vals)
dominant_freq = fft_freq[peak_idx]
```

#### Cálculos de Audio
- **Amplitud RMS**: `sqrt(mean(audio_data²))`
- **Nivel dB**: `20 * log10(rms / 32768.0)`
- **Normalización**: Escala de -1 a 1

### 3. Visualización Psicodélica

#### Colores Dinámicos
Los colores cambian según la frecuencia dominante:
```
Frecuencia → Color
─────────────────────
  100 Hz → #FF00FF (Magenta)
  200 Hz → #00FFFF (Cyan)
  440 Hz → #FFFF00 (Amarillo)
  880 Hz → #FF0080 (Rosa)
 1500 Hz → #00FF80 (Verde)
 3000 Hz → #8000FF (Violeta)
```

#### Dos Gráficos Sincronizados
1. **Onda Temporal** (superior)
   - Muestra la forma de onda en tiempo real
   - Actualización: 20 FPS
   - Color: Reactivo a frecuencia

2. **Espectro de Frecuencias** (inferior)
   - Muestra distribución de frecuencias (0-11025 Hz)
   - Color complementario al gráfico superior
   - Normalizado automáticamente

### 4. Interfaz de Terminal Rich

Muestra información en vivo:
```
╭───────────────────────────────────────╮
│  🎼 Analizador de Audio en Tiempo Real 🎼  │
├───────────────────────────────────────┤
│  🎵 Frecuencia:  440.2 Hz            │
│  📊 Amplitud:    0.7854              │
│  🔊 Nivel:       -12.3 dB            │
│  📈 Visual:      ████████████░░░░░░  │
╰───────────────────────────────────────╯
```

## Arquitectura Multihilo

### Hilos de Ejecución
1. **audio_capture_thread**: Captura continua de audio del micrófono
2. **rich_display_thread**: Actualiza terminal con estadísticas
3. **Main Thread**: Ejecuta animación de matplotlib

### Sincronización
- **Colas con límite**: Tamaño máximo de 10 elementos
- **put_nowait()**: No bloquea si la cola está llena
- **Threading.Event**: Permite shutdown graceful

### Manejo de Errores
- Excepciones capturadas y registradas
- Continúa operando ante errores temporales
- Shutdown limpio con Ctrl+C

## Flujo de Datos

```
Audio Input (Micrófono)
    ↓
PyAudio Stream (44.1kHz, 16-bit)
    ↓
Buffer (2048 samples)
    ↓
Normalización (-1 a 1)
    ↓
┌───────────────┴──────────────┐
│                              │
FFT Analysis             RMS Calculation
│                              │
Frecuencia Dominante     Amplitud & dB
│                              │
└───────────────┬──────────────┘
                ↓
        Estadísticas
                ↓
    ┌───────────┴──────────┐
    │                      │
Queue Viz           Queue Rich
    │                      │
Matplotlib          Terminal
Visualización       Display
```

## Optimizaciones

1. **Procesamiento Paralelo**: Tres hilos independientes
2. **Colas Acotadas**: Evita uso excesivo de memoria
3. **Hilos Daemon**: Terminan automáticamente al cerrar
4. **Ventana de Hanning**: Reduce artefactos en FFT
5. **Cache de Frames**: Deshabilitado para mejor performance

## Dependencias

- **numpy**: Operaciones numéricas y arrays
- **scipy**: FFT y procesamiento de señales
- **matplotlib**: Visualización gráfica animada
- **pyaudio**: Interfaz con hardware de audio
- **rich**: UI de terminal avanzada

## Casos de Uso

✅ Análisis de voz en tiempo real
✅ Visualización de música
✅ Educación en procesamiento de señales
✅ Debugging de audio
✅ Arte generativo sonoro
✅ DJ/VJ tools

## Notas de Implementación

### Rendimiento
- CPU: ~5-10% en procesador moderno
- Memoria: ~50-100 MB
- Latencia: <50ms

### Limitaciones
- Requiere hardware de audio funcional
- PortAudio debe estar instalado en el sistema
- Ventana de matplotlib debe permanecer abierta

### Compatibilidad
- Python 3.7+
- Linux, macOS, Windows
- Cualquier dispositivo de entrada de audio compatible
