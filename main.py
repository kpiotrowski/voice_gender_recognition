import glob
from scipy.io import wavfile
from pylab import *
from numpy import *
from scipy import *

maleFemaleFreq = [132, 210]

def HPS(rate, data):
    T = 1
    data = data[int(len(data)/2)-int(T*rate/2):int(len(data)/2)+int(T*rate/2)]
    window = np.hamming(T*rate)
    data = [d*w for d,w in zip(data,window)]
    fftV = abs(fft(data))/rate


    #freqs = linspace(0,rate, rate*T, endpoint=False)
    #stem(freqs, data, '-*')
    #show()
    #print(fftV)

    return 1

def simpleRecognition(rate, data):
    if(checkBaseFreq(maleFemaleFreq[0], rate, data) < checkBaseFreq(maleFemaleFreq[1], rate, data)): return 1
    return 0
def checkBaseFreq(freq, ratio, data):
    T=2
    box = int(1/freq*ratio)
    return average([listVariation(data[i*box:(i+1)*box-1],data[(i+1)*box:(i+2)*box-1]) for i in range(
        int(len(data)/box/2-(T/2*freq)),
        int(len(data)/box/2+(T/2*freq)),1)])
def listVariation(list1, list2): return sum([ abs(int(x)-int(y)) for x,y in zip(list1, list2)])

if __name__ == "__main__":
    wspMax = 0
    for MM in range(60,180,4):
        for K in range(160,280,4):
            maleFemaleFreq=[MM,K]

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
            #print(wsp)


            if(wsp-wspMax>0.0001):
                wspMax = wsp
                print("WSP: "+str(wsp)+" M: "+str(MM)+" K: "+str(K))
