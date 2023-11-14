import sounddevice as sd
import numpy as np
from scipy.fftpack import fft
from copy import copy
from tkinter import filedialog
import tkinter as tk

# Define la duración de la grabación en segundos
DURATION = 5

# Define la frecuencia de muestreo (en Hz)
SAMPLE_RATE = 44100

# Define los rangos de frecuencia para voces masculinas y femeninas
maleMinMax = (85, 180)
femaleMinMax = (165, 255)

# Define el umbral de detección de silencio
SILENCE_THRESHOLD = 0.01  # Ajusta este valor según sea necesario

# Define la función HPS
def HPS(rate, data):
    # Calcula la energía del audio
    energy = np.sum(np.abs(data))

    # Añade una comprobación de silencio
    if energy < SILENCE_THRESHOLD:
        return "Silence"

    # Normaliza los datos de audio
    data = data / np.max(np.abs(data))

    # Aplica la transformada de Fourier rápida (FFT)
    fft_result = abs(fft(data)) / rate

    # Calcula las sumas para los rangos de frecuencia masculina y femenina
    male_sum = sum(fft_result[maleMinMax[0]:maleMinMax[1]])
    female_sum = sum(fft_result[femaleMinMax[0]:femaleMinMax[1]])

    # Determina el género basado en las sumas
    if male_sum > female_sum:
        return "Male"
    return "Female"

# Función para seleccionar un archivo de audio
def choose_audio_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Seleccionar archivo de audio", filetypes=[("Archivos de audio", "*.wav;*.mp3")])
    return file_path

# Decide si usar el micrófono o cargar un archivo de audio
use_microphone = input("¿Usar el micrófono? (s/n): ").lower() == 's'

if use_microphone:
    # Utiliza el micrófono
    print("Usando el micrófono...")
    stream = sd.InputStream(callback=callback, channels=1, samplerate=SAMPLE_RATE)
    with stream:
        sd.sleep(int(DURATION * 1000))
else:
    # Cargar archivo de audio
    file_path = choose_audio_file()
    if file_path:
        print(f"Usando archivo de audio: {file_path}")
        data, rate = sd.read(file_path, dtype='float32')
        if len(data.shape) == 1:  # Mono audio
            gender = HPS(rate, data)
            print(f"Género detectado: {gender}")
        else:
            print("El archivo debe ser de un solo canal (mono).")
