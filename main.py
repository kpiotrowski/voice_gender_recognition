import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read
from scipy.fftpack import fft
from copy import copy


# Define la frecuencia de muestreo (en Hz)
SAMPLE_RATE = 44100

# Define los rangos de frecuencia para voces masculinas y femeninas
maleMinMax = (50, 180)
femaleMinMax = (165, 300)

# Define el número de iteraciones para el método HPS
HPSLoop = 5

# Define la función HPS
def HPS(rate, data):
    # Añade una comprobación de silencio
    if np.max(np.abs(data)) < 5e-4:
        return "Silence"
    # Normaliza los datos de audio
    data = data / np.max(np.abs(data))

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

    male_sum = sum(result[maleMinMax[0]:maleMinMax[1]])
    female_sum = sum(result[femaleMinMax[0]:femaleMinMax[1]])

    if male_sum > female_sum:
        return "Male"
    return "Female"
    
# Contadores para el recuento
male_count = 0
female_count = 0
silence_count = 0

def process_audio(file_path):
    global male_count, female_count, silence_count
    try:
        fs, audio_data = read(file_path)
        audio_data = audio_data.astype('float32') / np.max(np.abs(audio_data))  # Normaliza los datos de audio
        print(f"Duración del archivo: {len(audio_data) / fs:.2f} segundos")
        gender = HPS(fs, audio_data)
        print(f"Género detectado: {gender}")
        print("\n" + "="*30 + "\n")

        # Incrementa los contadores
        if gender == "Male":
            male_count += 1
        elif gender == "Female":
            female_count += 1
        elif gender == "Silence":
            silence_count += 1
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")

# Función de callback para micrófono
def callback(indata, frames, time, status):
    if status:
        print(f"Error en la captura de audio: {status}")
        return

    # Convierte los datos de audio a un array de NumPy
    data = np.frombuffer(indata, dtype=np.float32)

    # Aplica la función HPS a los datos de audio
    gender = HPS(SAMPLE_RATE, data)

    # Imprime el resultado
    print(f"Género detectado: {gender}")
    print("\n" + "="*30 + "\n")

# Pregunta al usuario si desea usar el micrófono o archivos de la carpeta "samples"
source_option = input("Seleccione 'm' para micrófono o 'a' para archivos en la carpeta 'samples': ")

if source_option == 'm':
    # Configuración para micrófono
    stream = sd.InputStream(callback=callback, channels=1, samplerate=SAMPLE_RATE)
    try:
        with stream:
            sd.sleep(5000)  # Captura durante 5 segundos
    except KeyboardInterrupt:
        print("\nCaptura de audio detenida por el usuario.")
    finally:
        if 'stream' in locals():
            stream.stop()
            stream.close()


elif source_option == 'a':
    # Configuración para cargar archivos de audio desde la carpeta "samples"
    samples_folder = "samples"
    for filename in os.listdir(samples_folder):
        if filename.endswith(".wav"):
            file_path = os.path.join(samples_folder, filename)
            try:
                fs, audio_data = read(file_path)  # Usa scipy.io.wavfile.read en lugar de sounddevice.read
                audio_data = audio_data.astype('float32') / np.max(np.abs(audio_data))  # Normaliza los datos de audio
                print(f"Procesando {file_path}...")
                gender = HPS(fs, audio_data)
                print(f"Género detectado: {gender}")
                print("\n" + "="*30 + "\n")
            except Exception as e:
                print(f"Error al procesar {file_path}: {e}")

print(f"Recuento final:")
print(f"Male: {male_count}")
print(f"Female: {female_count}")
print(f"Silence: {silence_count}")