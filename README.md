# ondasinusoidal 🎵

Una onda sinusoidal es una señal que sube y baja suavemente de manera repetitiva y perfecta, formando una curva continua. Representa un movimiento armónico simple: cada punto de la señal cambia con el tiempo siguiendo un patrón regular.

## Descripción

Este programa captura audio desde el micrófono en tiempo real, procesa la señal como una onda sinusoidal y la visualiza de forma dinámica con efectos psicodélicos. 

### Características

- **Captura de audio en tiempo real** desde el micrófono
- **Análisis de señal** con numpy y scipy:
  - Frecuencia dominante mediante FFT
  - Amplitud RMS
  - Nivel en decibelios
- **Visualización gráfica dinámica** con matplotlib:
  - Forma de onda sinusoidal en tiempo real
  - Espectro de frecuencias con FFT
  - Colores psicodélicos que reaccionan a la frecuencia
- **Interfaz de terminal** con rich:
  - Información en vivo de frecuencia, amplitud y nivel
  - Barra de nivel visual
  - Bordes de colores dinámicos

## Instalación

### Requisitos previos

- Python 3.7 o superior
- Micrófono funcional
- PortAudio (requerido por PyAudio)

#### Instalar PortAudio en Linux:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

#### Instalar PortAudio en macOS:
```bash
brew install portaudio
```

#### En Windows:
PyAudio debería funcionar directamente con pip.

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

Ejecutar el programa:

```bash
python3 ondasinusoidal.py
```

El programa abrirá dos ventanas:
1. **Terminal** - Muestra información en vivo sobre la señal de audio
2. **Ventana gráfica** - Visualización dinámica de la onda sinusoidal y el espectro

Habla, canta o reproduce música cerca del micrófono para ver los efectos visuales psicodélicos en acción.

Para salir, presiona `Ctrl+C` o cierra la ventana gráfica.

## Tecnologías utilizadas

- **numpy** - Análisis numérico y procesamiento de señales
- **matplotlib** - Visualización gráfica dinámica
- **pyaudio** - Captura de audio del micrófono
- **scipy** - Transformada de Fourier (FFT) para análisis de frecuencias
- **rich** - Interfaz de terminal con información en vivo

## Funcionamiento

1. El programa captura audio continuamente del micrófono en chunks de 2048 muestras
2. Cada chunk se analiza para extraer:
   - Frecuencia dominante usando FFT con ventana de Hanning
   - Amplitud RMS de la señal
   - Nivel en decibelios
3. Los datos se visualizan en tiempo real:
   - La forma de onda muestra la señal de audio
   - El espectro muestra las frecuencias presentes
   - Los colores cambian según la frecuencia dominante
4. La terminal muestra las métricas actualizadas 10 veces por segundo

## Características técnicas

- Frecuencia de muestreo: 44100 Hz
- Tamaño de buffer: 2048 muestras
- Tasa de refresco visual: 20 FPS
- Procesamiento multihilo para captura y visualización simultáneas
