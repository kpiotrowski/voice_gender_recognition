import glob
from scipy.io import wavfile

#male: 1 female: 0
shouldBeMale = 10
shouldBeFemale = 10
foundMale = 8
foundFemale = 12

files = glob.glob("samples/*.wav")
for file in files:



    array = wavfile.read(file)
    shouldBe = int(file.replace("/","_").replace(".","_").split("_")[2] == "M")


    print(str(shouldBe) + " : " + file + " " + str(array))


print("MACIERZ POKRYCIA:")
M = [ [min(shouldBeMale, foundMale), max(0,shouldBeMale-foundMale)], [max(0,shouldBeFemale-foundFemale), min(shouldBeFemale, foundFemale)] ]
wsp = (M[0][0]+M[1][1])/(sum(M[0])+sum(M[1]))
print(wsp)