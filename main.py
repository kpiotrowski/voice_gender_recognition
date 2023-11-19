import os
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import read
from scipy.fftpack import fft
from copy import copy
import shutil

SAMPLE_RATE = 44100

# Define los rangos de frecuencia para voces masculinas y femeninas
maleMinMax = (50, 175)
femaleMinMax = (165, 300)

# Define el número de iteraciones para el método HPS
HPSLoop = 6

# Contadores para el recuento
male_count = 0
female_count = 0
unknown_count = 0

# Variables globales para contar índices
male_index = 0
female_index = 0
unknown_index = 0

# Función HPS (sin cambios)
def HPS(rate, data):
    # Añade una comprobación de silencio
    if np.max(np.abs(data)) < 1e-1:
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

# Función para procesar audio
def process_audio(file_path, perform_rename=False):
    global male_count, female_count, unknown_count
    try:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.wav':
            fs, audio_data = read(file_path)
            # Convierte a mono si es estéreo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            audio_data = audio_data.astype('float32') / np.max(np.abs(audio_data))
        else:
            print(f"Formato no compatible para el archivo {file_path}")
            return

        print(f"Nombre del archivo: {os.path.basename(file_path)}")
        print(f"Duración del archivo: {len(audio_data) / fs:.2f} segundos")

        # Obtiene el género detectado por la función HPS
        gender = HPS(fs, audio_data)

        original_prediction = [1, 0] if gender == 'Male' else [0, 1] if gender == 'Female' else [0, 0]

        # Aplicar post-procesamiento
        smoothed_gender = post_process(original_prediction)

        # Aplicar post-procesamiento
        if smoothed_gender[0] > smoothed_gender[1]:
            male_count += 1
            result_gender = 'Male'
        elif smoothed_gender[1] > smoothed_gender[0]:
            female_count += 1
            result_gender = 'Female'
        else:
            unknown_count += 1
            result_gender = 'Unknown'

        print(f"Género detectado (original): {gender}")
        print(f"Género detectado (suavizado): {result_gender}")
        print("\n" + "=" * 30 + "\n")

        if perform_rename:
            # Realiza el renombrado automáticamente
            rename_file(file_path, result_gender)

    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")

# Función para renombrar un archivo
def rename_file(file_path, gender):
    global male_index, female_index, unknown_index

    # Configuración para cargar archivos de audio desde la carpeta especificada
    output_folder = "output"

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Genera el nuevo nombre del archivo en función del género
    if gender == 'Male':
        new_filename = f"{male_index:02d}_Male.wav"
        male_index += 1
    elif gender == 'Female':
        new_filename = f"{female_index:02d}_Female.wav"
        female_index += 1
    else:
        new_filename = f"{unknown_index:02d}_Unknown.wav"
        unknown_index += 1

    new_file_path = os.path.join(output_folder, new_filename)

    # Si es renombrado automáticamente, no pregunta si debe sobrescribir
    if not os.path.exists(new_file_path):
        shutil.copy2(file_path, new_file_path)
        print(f"Archivo renombrado y copiado automáticamente: {new_filename}")
    else:
        # Pregunta si desea sobrescribir si el archivo ya existe
        overwrite_option = input(f"El archivo {new_filename} ya existe. ¿Desea sobrescribirlo? (y/n): ")
        if overwrite_option.lower() == 'y':
            shutil.copy2(file_path, new_file_path)
            print(f"Archivo renombrado y copiado: {new_filename}")
        else:
            print(f"El archivo {os.path.basename(file_path)} no se ha renombrado.")

# Función para suavizar la predicción
def post_process(prediction):
    # Implementa aquí tu lógica de suavizado
    return prediction

# Función de callback para micrófono
def callback(indata, frames, time, status):
    if status:
        print(f"Error en la captura de audio: {status}")
        return

    # Convierte los datos de audio a un array de NumPy
    data = np.frombuffer(indata, dtype=np.float32)
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Aplica la función HPS a los datos de audio
    gender = HPS(SAMPLE_RATE, data)

    # Imprime el resultado
    print(f"Género detectado: {gender}")
    print("\n" + "="*30 + "\n")

# Función principal para analizar el micrófono
def analyze_microphone():
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

# Función principal para analizar y renombrar archivos automáticamente
def analyze_and_rename_audio_files(folder_path):
    global male_index, female_index, unknown_index, male_count, female_count, unknown_count
    # Reinicia los contadores y los índices al comienzo
    male_count = 0
    female_count = 0
    unknown_count = 0
    male_index = 0
    female_index = 0
    unknown_index = 0
    
    # Imprime el recuento final
    print(f"Recuento final:")
    print(f"Male: {male_count}")
    print(f"Female: {female_count}")
    print(f"Silence or unknown: {unknown_count}")

    # Itera sobre los archivos procesados
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Procesa el audio
        process_audio(file_path, perform_rename=True)

    # Imprime el recuento final después de la actualización
    print(f"Recuento final después de la actualización:")
    print(f"Male: {male_count}")
    print(f"Female: {female_count}")
    print(f"Silence or unknown: {unknown_count}")

def analyze_audio_files(folder_path):
    global male_count, female_count, unknown_count
    # Imprime el recuento final antes de la iteración
    print(f"Recuento final antes de la iteración:")
    print(f"Male: {male_count}")
    print(f"Female: {female_count}")
    print(f"Silence or unknown: {unknown_count}")

    # Itera sobre los archivos en la carpeta
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Procesa el audio sin realizar el renombrado
        process_audio(file_path)

    # Imprime el recuento final después de la iteración
    print(f"Recuento final después de la iteración:")
    print(f"Male: {male_count}")
    print(f"Female: {female_count}")
    print(f"Silence or unknown: {unknown_count}")

# Función principal para renombrar archivos manualmente
def rename_files_manually(input_folder):
    global male_index, female_index, unknown_index
    # Configuración para cargar archivos de audio desde la carpeta especificada
    output_folder = "output_manual"

    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Pregunta al usuario el nuevo nombre
        new_filename = input(f"Ingrese el nuevo nombre para {filename}: ")

        # Genera el nuevo nombre del archivo en función del género
        if "Male" in filename:
            new_filename = f"{new_filename}.wav"
            male_index += 1
        elif "Female" in filename:
            new_filename = f"{new_filename}.wav"
            female_index += 1
        else:
            new_filename = f"{new_filename}.wav"
            unknown_index += 1

        new_file_path = os.path.join(output_folder, new_filename)

        # Pregunta si desea sobrescribir si el archivo ya existe
        if os.path.exists(new_file_path):
            overwrite_option = input(f"El archivo {new_filename} ya existe. ¿Desea sobrescribirlo? (y/n): ")
            if overwrite_option.lower() != 'y':
                print(f"El archivo {filename} no se ha renombrado.")
                continue

        shutil.copy2(file_path, new_file_path)
        print(f"Archivo renombrado: {new_filename}")
        print("\n" + "=" * 30 + "\n")


while True:
    print("Menu Principal:")
    print("1. Analizar audio")
    print("2. Analizar y renombrar audio automáticamente")
    print("3. Renombrar archivo manualmente")
    print("0. Salir")

    option = input("Seleccione una opción (0-3): ")

    if option == "0":
        break
    elif option == "1":
        print("Seleccione el tipo de análisis:")
        print("a. Analizar archivos de audio")
        print("m. Analizar audio del micrófono")
        
        analysis_option = input("Seleccione una opción (a/m): ")

        if analysis_option == "a":
            folder_path = input("Ingrese la ruta de la carpeta de archivos de audio: ")
            analyze_audio_files(folder_path)
        elif analysis_option =="m":
            analyze_microphone()
        else:
            print("Opción no válida.")

    elif option == "2":
        folder_path = input("Ingrese la ruta de la carpeta de archivos de audio: ")
        analyze_and_rename_audio_files(folder_path)

    elif option == "3":
        input_folder = input("Ingrese la ruta de la carpeta de archivos de audio a renombrar manualmente: ")
        rename_files_manually(input_folder)

    else:
        print("Opción no válida. Inténtelo de nuevo.")
