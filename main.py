import sounddevice as sd
import numpy as np
from scipy.fftpack import fft

# Define la duración de la grabación en segundos
DURATION = 5

# Define la frecuencia de muestreo (en Hz)
SAMPLE_RATE = 44100

# Define los rangos de frecuencia para voces masculinas y femeninas
maleMinMax = (85, 170)
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

# Define la función de callback que se llamará para cada bloque de audio
def callback(indata, frames, time, status):
    if status:
        print(f"Error en la captura de audio: {status}")
        return

    # Convierte los datos de audio a un array de NumPy
    data = np.frombuffer(indata, dtype=np.float32)

    # Aplica la función HPS a los datos de audio
    gender = HPS(SAMPLE_RATE, data)

    # Imprime el resultado
    print(gender)

# Crea un objeto de entrada de audio con la función de callback
stream = sd.InputStream(callback=callback, channels=1, samplerate=SAMPLE_RATE)

# Inicia la captura de audio
with stream:
    sd.sleep(int(DURATION * 1000))
