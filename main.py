import glob
from scipy.io import wavfile

files = glob.glob("samples/*.wav")
i = 0
for file in files:
    i += 1
    print(file)
    array = wavfile.read(file)

    print(str(i) + " : " + file + " " + str(array))


print("KONIEC")
