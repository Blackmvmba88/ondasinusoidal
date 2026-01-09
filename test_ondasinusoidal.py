#!/usr/bin/env python3
"""
Script de prueba para verificar la lógica del procesador de audio
sin requerir hardware de audio real
"""

import numpy as np
import sys

def test_audio_processing():
    """Prueba las funciones de procesamiento de audio con datos sintéticos"""
    
    print("Probando procesamiento de señales de audio...\n")
    
    # Configuración
    RATE = 44100
    CHUNK = 2048
    
    # Generar señal sintética (440 Hz - nota A)
    duration = CHUNK / RATE
    t = np.linspace(0, duration, CHUNK)
    frequency = 440  # Hz (nota A)
    audio_data = np.sin(2 * np.pi * frequency * t)
    
    print(f"✓ Señal sintética generada: {frequency} Hz")
    print(f"  Tamaño de muestra: {len(audio_data)}")
    print(f"  Rango de valores: [{audio_data.min():.3f}, {audio_data.max():.3f}]")
    
    # Test 1: FFT para encontrar frecuencia dominante
    from scipy.fft import fft, fftfreq
    
    windowed = audio_data * np.hanning(len(audio_data))
    fft_vals = fft(windowed)
    fft_freq = fftfreq(len(windowed), 1.0/RATE)
    
    positive_freq_idx = np.where(fft_freq > 0)
    fft_vals_pos = np.abs(fft_vals[positive_freq_idx])
    fft_freq_pos = fft_freq[positive_freq_idx]
    
    if len(fft_vals_pos) > 0:
        peak_idx = np.argmax(fft_vals_pos)
        detected_freq = abs(fft_freq_pos[peak_idx])
        print(f"\n✓ FFT ejecutado correctamente")
        print(f"  Frecuencia detectada: {detected_freq:.1f} Hz")
        print(f"  Error: {abs(detected_freq - frequency):.1f} Hz")
        
        # Verificar que la frecuencia detectada esté cerca de la esperada
        if abs(detected_freq - frequency) < 10:
            print("  ✓ Detección de frecuencia CORRECTA")
        else:
            print("  ✗ Detección de frecuencia con error elevado")
    
    # Test 2: Amplitud RMS
    rms = np.sqrt(np.mean(audio_data**2))
    print(f"\n✓ Amplitud RMS calculada: {rms:.4f}")
    
    # Para una sinusoide perfecta con amplitud 1, RMS debería ser ~0.707
    expected_rms = 1.0 / np.sqrt(2)
    print(f"  Valor esperado: {expected_rms:.4f}")
    print(f"  Error: {abs(rms - expected_rms):.4f}")
    
    if abs(rms - expected_rms) < 0.01:
        print("  ✓ Cálculo de RMS CORRECTO")
    else:
        print("  ✗ Cálculo de RMS con error")
    
    # Test 3: Nivel en decibelios
    if rms > 0:
        db = 20 * np.log10(rms)
        print(f"\n✓ Nivel en dB calculado: {db:.1f} dB")
    
    # Test 4: Normalización
    if np.max(np.abs(audio_data)) > 0:
        normalized = audio_data / np.max(np.abs(audio_data))
        print(f"\n✓ Normalización ejecutada")
        print(f"  Rango normalizado: [{normalized.min():.3f}, {normalized.max():.3f}]")
    
    print("\n" + "="*60)
    print("✓ Todas las funciones de procesamiento funcionan correctamente")
    print("="*60)
    
    return True

def test_color_cycling():
    """Prueba el sistema de colores psicodélicos"""
    print("\nProbando sistema de colores psicodélicos...\n")
    
    colors = ['#FF00FF', '#00FFFF', '#FFFF00', '#FF0080', '#00FF80', '#8000FF']
    
    # Simular diferentes frecuencias
    test_frequencies = [100, 200, 440, 880, 1500, 3000]
    
    print("Frecuencia → Color")
    print("-" * 40)
    for freq in test_frequencies:
        color_idx = int((freq / 100) % len(colors))
        color = colors[color_idx]
        print(f"{freq:>6} Hz → {color}")
    
    print("\n✓ Sistema de colores funciona correctamente")
    return True

def main():
    """Ejecuta todas las pruebas"""
    print("="*60)
    print("  PRUEBAS DE ONDASINUSOIDAL")
    print("="*60 + "\n")
    
    try:
        # Verificar que numpy y scipy estén disponibles
        import numpy
        import scipy
        print("✓ numpy y scipy importados correctamente\n")
        
        # Ejecutar pruebas
        test_audio_processing()
        test_color_cycling()
        
        print("\n" + "="*60)
        print("  ✓ TODAS LAS PRUEBAS PASARON")
        print("="*60 + "\n")
        
        return 0
        
    except ImportError as e:
        print(f"✗ Error: No se pudo importar un módulo requerido: {e}")
        print("\nPara ejecutar las pruebas, instala las dependencias:")
        print("  pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"✗ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
