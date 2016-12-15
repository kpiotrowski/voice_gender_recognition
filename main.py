import glob
from scipy.io import wavfile


def HPS(array):


    return 1


if __name__ == "__main__":
    # male: 1 female: 0
    shouldBe = [0,0]
    found = [0,0]
    files = glob.glob("samples/*.wav")
    for file in files:
        array = wavfile.read(file)
        shouldBe[int(file.replace("/", "_").replace(".", "_").split("_")[2] == "M")]+=1


        print(str(shouldBe) + " : " + file + " " + str(array))

    print("MACIERZ POKRYCIA:")
    M = [[min(shouldBe[1], found[1]), max(0, shouldBe[1] - found[1])],
         [max(0, shouldBe[0] - found[0]), min(shouldBe[0], found[0])]]
    print(M)
    wsp = (M[0][0] + M[1][1]) / (sum(M[0]) + sum(M[1]))
    print(wsp)
