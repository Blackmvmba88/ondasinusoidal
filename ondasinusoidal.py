#!/usr/bin/env python3
"""
Programa de captura y visualización de audio en tiempo real
Captura audio del micrófono, procesa la señal como onda sinusoidal
y visualiza de forma dinámica con efectos psicodélicos
"""

import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal
from scipy.fft import fft, fftfreq
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.table import Table
import threading
import queue
import warnings
warnings.filterwarnings('ignore')

# Configuración de audio
CHUNK = 2048  # Tamaño del buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Frecuencia de muestreo

# Cola para comunicación entre hilos
audio_queue = queue.Queue()
stats_queue = queue.Queue()

class AudioProcessor:
    """Procesa el audio capturado y extrae características"""
    
    def __init__(self, rate=RATE, chunk=CHUNK):
        self.rate = rate
        self.chunk = chunk
        self.console = Console()
        
    def get_dominant_frequency(self, audio_data):
        """Calcula la frecuencia dominante usando FFT"""
        # Aplicar ventana de Hanning para reducir el efecto de bordes
        windowed = audio_data * np.hanning(len(audio_data))
        
        # Calcular FFT
        fft_vals = fft(windowed)
        fft_freq = fftfreq(len(windowed), 1.0/self.rate)
        
        # Tomar solo frecuencias positivas
        positive_freq_idx = np.where(fft_freq > 0)
        fft_vals = np.abs(fft_vals[positive_freq_idx])
        fft_freq = fft_freq[positive_freq_idx]
        
        # Encontrar frecuencia dominante
        if len(fft_vals) > 0:
            peak_idx = np.argmax(fft_vals)
            dominant_freq = fft_freq[peak_idx]
            return abs(dominant_freq)
        return 0.0
    
    def get_amplitude(self, audio_data):
        """Calcula la amplitud RMS"""
        rms = np.sqrt(np.mean(audio_data**2))
        return rms
    
    def get_level_db(self, audio_data):
        """Calcula el nivel en decibelios"""
        rms = self.get_amplitude(audio_data)
        if rms > 0:
            db = 20 * np.log10(rms / 32768.0)  # Normalizado a 16-bit
            return max(db, -60)  # Limitar a -60dB mínimo
        return -60

def audio_capture_thread():
    """Hilo para captura continua de audio"""
    p = pyaudio.PyAudio()
    
    try:
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        processor = AudioProcessor()
        
        while True:
            try:
                # Leer datos de audio
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                
                # Normalizar
                if np.max(np.abs(audio_data)) > 0:
                    audio_data = audio_data / np.max(np.abs(audio_data))
                
                # Procesar características
                freq = processor.get_dominant_frequency(audio_data)
                amplitude = processor.get_amplitude(audio_data)
                level_db = processor.get_level_db(audio_data)
                
                # Enviar datos a las colas
                audio_queue.put(audio_data)
                stats_queue.put({
                    'frequency': freq,
                    'amplitude': amplitude,
                    'level_db': level_db
                })
                
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"Error en captura de audio: {e}")
    finally:
        if stream.is_active():
            stream.stop_stream()
        stream.close()
        p.terminate()

def create_rich_display(stats):
    """Crea el display de Rich con información en vivo"""
    layout = Layout()
    
    # Crear tabla con estadísticas
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="cyan bold")
    table.add_column(style="magenta bold")
    
    freq = stats.get('frequency', 0.0)
    amp = stats.get('amplitude', 0.0)
    level = stats.get('level_db', -60)
    
    # Agregar filas con información
    table.add_row("🎵 Frecuencia:", f"{freq:.1f} Hz")
    table.add_row("📊 Amplitud:", f"{amp:.4f}")
    table.add_row("🔊 Nivel:", f"{level:.1f} dB")
    
    # Crear barra de nivel visual
    level_normalized = max(0, min(100, (level + 60) * 100 / 60))
    bar_length = int(level_normalized / 5)
    bar = "█" * bar_length + "░" * (20 - bar_length)
    table.add_row("📈 Visual:", bar)
    
    # Panel con estilo psicodélico
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
    color_idx = int((freq / 100) % len(colors))
    border_color = colors[color_idx]
    
    panel = Panel(
        table,
        title="[bold white]🎼 Analizador de Audio en Tiempo Real 🎼[/bold white]",
        border_style=border_color,
        padding=(1, 2)
    )
    
    return panel

class PsychedelicVisualizer:
    """Visualizador con efectos psicodélicos"""
    
    def __init__(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.fig.patch.set_facecolor('#0a0a0a')
        
        # Configurar ejes
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('#1a1a1a')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('#333333')
            ax.spines['top'].set_color('#333333')
            ax.spines['left'].set_color('#333333')
            ax.spines['right'].set_color('#333333')
        
        # Eje superior: forma de onda
        self.ax1.set_title('Forma de Onda Sinusoidal', color='white', fontsize=14, fontweight='bold')
        self.ax1.set_xlabel('Tiempo (muestras)', color='white')
        self.ax1.set_ylabel('Amplitud', color='white')
        self.ax1.set_ylim(-1.1, 1.1)
        self.ax1.set_xlim(0, CHUNK)
        self.ax1.grid(True, alpha=0.2, color='cyan')
        
        # Eje inferior: espectro de frecuencias
        self.ax2.set_title('Espectro de Frecuencias', color='white', fontsize=14, fontweight='bold')
        self.ax2.set_xlabel('Frecuencia (Hz)', color='white')
        self.ax2.set_ylabel('Magnitud', color='white')
        self.ax2.set_xlim(0, RATE // 4)  # Mostrar hasta 1/4 de la frecuencia de muestreo
        self.ax2.set_ylim(0, 1)
        self.ax2.grid(True, alpha=0.2, color='magenta')
        
        # Líneas para dibujar
        self.line1, = self.ax1.plot([], [], linewidth=2)
        self.line2, = self.ax2.plot([], [], linewidth=2)
        
        # Colores psicodélicos
        self.colors = ['#FF00FF', '#00FFFF', '#FFFF00', '#FF0080', '#00FF80', '#8000FF']
        self.color_idx = 0
        
        # Buffer para suavizado
        self.audio_buffer = np.zeros(CHUNK)
        
    def update_colors(self, frequency):
        """Actualiza colores basados en la frecuencia"""
        self.color_idx = int((frequency / 100) % len(self.colors))
        color = self.colors[self.color_idx]
        self.line1.set_color(color)
        
        # Color complementario para el espectro
        comp_idx = (self.color_idx + 3) % len(self.colors)
        self.line2.set_color(self.colors[comp_idx])
    
    def animate(self, frame):
        """Función de animación llamada en cada frame"""
        try:
            # Obtener datos de audio
            if not audio_queue.empty():
                self.audio_buffer = audio_queue.get()
            
            # Obtener estadísticas
            if not stats_queue.empty():
                stats = stats_queue.get()
                frequency = stats['frequency']
                self.update_colors(frequency)
            
            # Actualizar forma de onda
            x = np.arange(len(self.audio_buffer))
            self.line1.set_data(x, self.audio_buffer)
            
            # Calcular y actualizar espectro FFT
            fft_vals = fft(self.audio_buffer * np.hanning(len(self.audio_buffer)))
            fft_freq = fftfreq(len(self.audio_buffer), 1.0/RATE)
            
            # Solo frecuencias positivas
            positive_freq_idx = np.where((fft_freq > 0) & (fft_freq < RATE // 4))
            fft_vals = np.abs(fft_vals[positive_freq_idx])
            fft_freq = fft_freq[positive_freq_idx]
            
            # Normalizar espectro
            if len(fft_vals) > 0 and np.max(fft_vals) > 0:
                fft_vals = fft_vals / np.max(fft_vals)
            
            self.line2.set_data(fft_freq, fft_vals)
            
            return self.line1, self.line2
            
        except Exception as e:
            return self.line1, self.line2
    
    def start(self):
        """Inicia la animación"""
        ani = animation.FuncAnimation(
            self.fig,
            self.animate,
            interval=50,  # 20 FPS
            blit=True,
            cache_frame_data=False
        )
        plt.tight_layout()
        plt.show()

def rich_display_thread():
    """Hilo para mostrar información con Rich"""
    console = Console()
    
    with Live(console=console, refresh_per_second=10) as live:
        while True:
            try:
                if not stats_queue.empty():
                    stats = stats_queue.get()
                    display = create_rich_display(stats)
                    live.update(display)
            except Exception as e:
                continue

def main():
    """Función principal"""
    console = Console()
    
    # Mensaje de bienvenida
    console.print("\n[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold magenta]     🎵 Visualizador de Ondas Sinusoidales en Tiempo Real 🎵[/bold magenta]")
    console.print("[bold cyan]═══════════════════════════════════════════════════════════[/bold cyan]\n")
    
    console.print("[yellow]Iniciando captura de audio...[/yellow]")
    console.print("[green]Presiona Ctrl+C para salir[/green]\n")
    
    # Iniciar hilo de captura de audio
    audio_thread = threading.Thread(target=audio_capture_thread, daemon=True)
    audio_thread.start()
    
    # Iniciar hilo de display Rich
    display_thread = threading.Thread(target=rich_display_thread, daemon=True)
    display_thread.start()
    
    # Pequeña pausa para que se inicialice la captura
    import time
    time.sleep(1)
    
    # Iniciar visualización matplotlib
    try:
        visualizer = PsychedelicVisualizer()
        visualizer.start()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cerrando visualizador...[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
    finally:
        console.print("[green]¡Hasta luego![/green]\n")

if __name__ == "__main__":
    main()
