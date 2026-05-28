# Resonance Observatory — ondasinusoidal 🎵🌊

> **Un laboratorio ligero para observar sonido, frecuencia y resonancia en tiempo real.**

`ondasinusoidal` nació como un visualizador de ondas senoidales, pero su verdadero potencial está en algo más grande: convertir señales acústicas vivas en geometría, métricas e intuición física.

Este repositorio captura audio desde el micrófono, analiza su contenido espectral y lo transforma en visualizaciones dinámicas. Es una base práctica para explorar DSP, FFT, resonancia, armónicos, presión sonora y comportamiento ondulatorio.

---

## Visión

Una onda no es solo una curva: es una forma de energía organizada.

Este proyecto busca funcionar como un **observatorio de resonancia**:

- escuchar una señal viva,
- descomponerla en frecuencia,
- medir su amplitud y energía,
- visualizar su movimiento,
- detectar patrones armónicos,
- y construir intuición sobre cómo el sonido se comporta como fenómeno físico.

En términos simples:

```txt
micrófono → señal temporal → FFT → espectro → métricas → visualización
```

En términos de arquitectura:

```txt
Input Field
   ↓
Signal Acquisition
   ↓
Spectral Decomposition
   ↓
Resonance Mapping
   ↓
Visual Cognition Layer
```

---

## Características actuales

- **Captura de audio en tiempo real** desde micrófono.
- **Procesamiento de señal** con `numpy` y `scipy`.
- **FFT** para detectar frecuencia dominante.
- **Cálculo de amplitud RMS**.
- **Nivel en decibelios**.
- **Visualización dinámica** con `matplotlib`.
- **Forma de onda en tiempo real**.
- **Espectro de frecuencias**.
- **Colores reactivos** según la frecuencia dominante.
- **Interfaz en terminal** con `rich`.
- **Procesamiento multihilo** para captura y visualización simultáneas.

---

## Fundamento físico

Una onda sinusoidal representa movimiento armónico simple:

```txt
x(t) = A sin(2πft + φ)
```

Donde:

| Símbolo | Significado |
|---|---|
| `A` | Amplitud |
| `f` | Frecuencia |
| `t` | Tiempo |
| `φ` | Fase |

La idea central es que cualquier sonido complejo puede entenderse como una combinación de componentes sinusoidales. La FFT permite descomponer la señal y observar sus frecuencias internas.

---

## Instalación

### Requisitos

- Python 3.7 o superior
- Micrófono funcional
- PortAudio

### Linux

```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

### macOS

```bash
brew install portaudio
```

### Dependencias Python

```bash
pip install -r requirements.txt
```

---

## Uso

```bash
python3 ondasinusoidal.py
```

El programa abre dos interfaces:

1. **Terminal** — muestra métricas en vivo.
2. **Ventana gráfica** — muestra forma de onda y espectro.

Prueba con:

- voz,
- canto,
- palmadas,
- música,
- bajos/subgraves,
- tonos puros,
- instrumentos acústicos.

Para salir:

```bash
Ctrl+C
```

O cierra la ventana gráfica.

---

## Métricas observadas

| Métrica | Función |
|---|---|
| Frecuencia dominante | Detecta el pico principal del espectro |
| RMS | Estima energía/amplitud efectiva |
| dB | Mide nivel relativo de señal |
| FFT spectrum | Revela armónicos y distribución frecuencial |
| Waveform | Muestra el comportamiento temporal |

---

## Parámetros técnicos

| Parámetro | Valor |
|---|---|
| Sample rate | `44100 Hz` |
| Buffer size | `2048` muestras |
| Visual refresh | `20 FPS` |
| Terminal refresh | `10 Hz` |
| Procesamiento | Multihilo |

---

## Tecnologías

- `numpy` — análisis numérico.
- `scipy` — FFT y procesamiento de señal.
- `matplotlib` — visualización gráfica.
- `pyaudio` — captura de audio.
- `rich` — terminal interactiva.

---

## Roadmap conceptual

### Phase 1 — Signal Observatory ✅

Base actual:

- captura de audio,
- FFT,
- RMS,
- decibeles,
- visualización en vivo.

### Phase 2 — Harmonic Intelligence 🔄

Próximos módulos posibles:

- detección de armónicos,
- clasificación de energía sonora,
- detección de subgraves,
- medición de ruido,
- tracking de frecuencia en el tiempo.

### Phase 3 — Cymatics Mode 📋

Visualización física inspirada en cimática:

- nodos,
- patrones circulares,
- partículas reactivas,
- geometría emergente desde frecuencia.

### Phase 4 — Music Physics 📋

Herramientas para producción musical:

- kick/sub analyzer,
- tonal center detector,
- spectral density,
- stereo field map,
- transient detection.

### Phase 5 — Archimedes Bridge 📋

Conexión futura con laboratorios de resonancia física:

- osciladores clásicos,
- modos resonantes,
- absorción,
- coherencia,
- visualización avanzada de campos.

---

## Filosofía

Este repo no busca solamente dibujar ondas bonitas.

Busca convertir audio en una forma de observación:

```txt
escuchar → medir → visualizar → comprender
```

La señal se vuelve geometría.
La frecuencia se vuelve estructura.
El sonido se vuelve laboratorio.

---

## Estado

Proyecto funcional en Python.

Base estable para experimentos de audio, visualización, resonancia y análisis espectral.

---

## Autor

Desarrollado por **BlackMamba / Iyari Gomez**.

Parte del ecosistema creativo-técnico BlackMamba: música, física, visualización, resonancia y sistemas inteligentes.
