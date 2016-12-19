import glob
from scipy.io import wavfile
from pylab import *
from scipy import *

maleFemaleFreq = [120, 232]
TS=3 #time for simple method

humanVoiceMinMAx = [80,255]
maleMinMax=[60,160]
femaleMinMax=[180,270]
HPSLoop=5

def HPS(rate, dataVoice):
    T = 3  # time for HPS method

    if( T >len(dataVoice)/rate): T = len(dataVoice)/rate
    dataVoice = dataVoice[max(0, int(len(dataVoice) / 2) - int(T / 2 * rate)):min(len(dataVoice) - 1, int(len(dataVoice) / 2) + int(T / 2 * rate))]
    partLen=int(rate)
    parts = [ dataVoice[i*partLen:(i+1)*partLen] for i in range(int(T))]
    resultParts = []
    for data in parts:
        if(len(data)==0): continue
        window = np.hamming(len(data))
        data = data*window
        fftV = abs(fft(data))/rate
        fftR = copy(fftV)
        for i in range(2,HPSLoop):
            tab = copy(fftV[::i])
            fftR = fftR[:len(tab)]
            fftR *= tab
        resultParts.append(fftR)
    result = [0]*len(resultParts[int(len(resultParts)/2)])
    for res in resultParts:
        if(len(res)!=len(result)): continue
        result += res

    if(sum(result[maleMinMax[0]:maleMinMax[1]]) > sum(result[femaleMinMax[0]:femaleMinMax[1]])): return 1
    return 0

def simpleRecognition(rate, data):
    if(checkBaseFreq(maleFemaleFreq[0], rate, data) < checkBaseFreq(maleFemaleFreq[1], rate, data)): return 1
    return 0
def checkBaseFreq(freq, ratio, data):
    box = int(1/freq*ratio)
    return sum([listVariation(data[int(i*box):int((i+1)*box-1)],data[int((i+1)*box):int((i+2)*box-1)]) for i in range( max(0,int(len(data)/box/2-(TS/2*freq))), min(int(len(data)/box)-2,int(len(data)/box/2+(TS/2*freq))),1)])
def listVariation(list1, list2): return sum([ abs(int(x)-int(y)) for x,y in zip(list1, list2)])

if __name__ == "__main__":
    # male: 1 female: 0
    M = [[0,0],[0,0]]
    files = glob.glob("samples/*.wav")
    for file in files:
        rate, array = wavfile.read(file)
        shouldBe = int(file.replace("/", "_").replace(".", "_").split("_")[2] == "M")
        found = HPS(rate, array)
        #found = simpleRecognition(rate, array)
        M[shouldBe][found]+=1
    print(M)
    wsp = (M[0][0] + M[1][1]) / (sum(M[0]) + sum(M[1]))
    print(wsp)