import glob
from scipy.io import wavfile
from pylab import *
from scipy import *

maleFemaleFreq = [120, 232]
TS=3 #time for simple method

humanVoiceMinMAx = [80,255]
maleFemaleThreshold = 160
T=2.5 #time for HPS method
HPSLoop=10

def HPS(rate, data):
    data = data[max(0,int(len(data)/2)-int(T/2*rate)):min( len(data)-1,int(len(data)/2)+int(T/2*rate))]
    window = np.hamming(len(data))
    data = data*window
    fftV = abs(fft(data)[:int(rate/2)])
    fftR = copy(fftV)
    for i in range(2,HPSLoop):
        tab = copy(fftV[::i])
        fftR = fftR[:len(tab)]
        fftR *= tab
    fftR = fftR[humanVoiceMinMAx[0]:humanVoiceMinMAx[1]]
    maxFreq=argmax(fftR)+humanVoiceMinMAx[0]
    print(str(maxFreq))

    if (maxFreq<maleFemaleThreshold): return 1
    return 0

def simpleRecognition(rate, data):
    if(checkBaseFreq(maleFemaleFreq[0], rate, data) < checkBaseFreq(maleFemaleFreq[1], rate, data)): return 1
    return 0
def checkBaseFreq(freq, ratio, data):
    box = int(1/freq*ratio)
    return sum([listVariation(data[int(i*box):int((i+1)*box-1)],data[int((i+1)*box):int((i+2)*box-1)]) for i in range(
        max(0,int(len(data)/box/2-(TS/2*freq))),
        int(len(data)/box/2+(TS/2*freq)),1)])
def listVariation(list1, list2): return sum([ abs(int(x)-int(y)) for x,y in zip(list1, list2)])

if __name__ == "__main__":
    #wspMax = 0
    # for MM in range(119,122,1):
    #     for K in range(232,235,1):
    #         maleFemaleFreq=[MM,K]

    # male: 1 female: 0
    M = [[0,0],[0,0]]
    files = glob.glob("samples/*.wav")
    for file in files:
        rate, array = wavfile.read(file)
        shouldBe = int(file.replace("/", "_").replace(".", "_").split("_")[2] == "M")
        #found = HPS(rate, array)
        found = simpleRecognition(rate, array)
        #print(found)
        M[shouldBe][found]+=1
    #print("MACIERZ POKRYCIA:")
    #print(M)
    wsp = (M[0][0] + M[1][1]) / (sum(M[0]) + sum(M[1]))
    print(wsp)

            #
            # if(wsp-wspMax>0.0001):
            #    wspMax = wsp
            #    print("WSP: "+str(wsp)+" M: "+str(MM)+" K: "+str(K))
