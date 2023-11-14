import sounddevice as sd
import numpy as np
from scipy.fftpack import fft
from copy import copy

# Define la duración de la grabación en segundos
DURATION = 5

# Define la frecuencia de muestreo (en Hz)
SAMPLE_RATE = 44100

# Define los rangos de frecuencia para voces masculinas y femeninas
maleMinMax = (75, 150)
femaleMinMax = (150, 255)

# Define el número de iteraciones para el método HPS
HPSLoop = 5

# Define la función HPS
def HPS(rate, data):
    dataVoice = data
    T = 3  # time for HPS method

    if T > len(dataVoice) / rate:
        T = len(dataVoice) / rate
    dataVoice = dataVoice[max(0, int(len(dataVoice) / 2) - int(T / 2 * rate)):min(len(dataVoice) - 1, int(len(dataVoice) / 2) + int(T / 2 * rate))]
    partLen = int(rate)
    parts = [dataVoice[i * partLen:(i + 1) * partLen] for i in range(int(T))]
    resultParts = []
    
    fftR = np.zeros(len(dataVoice))  # Inicializa fftR aquí

    for data in parts:
        window = np.hamming(len(data))
        data = data * window
        fftV = abs(fft(data)) / rate
        fftR = copy(fftV)
        for i in range(2, HPSLoop):
            tab = copy(fftV[::i])
            fftR = fftR[:len(tab)]
            fftR *= tab
        resultParts.append(fftR)

    # Asegúrate de que resultParts tenga al menos un elemento
    if not resultParts:
        resultParts.append(np.zeros(len(fftR)))

    result = np.zeros(len(resultParts[0]))

    for res in resultParts:
        if len(res) != len(result):
            continue
        result = np.add(result, res)

    if sum(result[maleMinMax[0]:maleMinMax[1]]) > sum(result[femaleMinMax[0]:femaleMinMax[1]]):
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

    # Aquí puedes hacer algo con el resultado (por ejemplo, imprimirlo)
    print(gender)

# Crea un objeto de entrada de audio con la función de callback
stream = sd.InputStream(callback=callback, channels=1, samplerate=SAMPLE_RATE)

# Inicia la captura de audio
with stream:
    sd.sleep(int(DURATION * 1000))
