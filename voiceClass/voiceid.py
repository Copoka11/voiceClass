
import pyaudio
import wave
import sys
import numpy as np  
import matplotlib.pyplot as plt

#file = open("params.txt", 'r')
#number = int(file.readline())
#print(number)
#file.close()

class voiceRec:
       
    CHUNK = 1024                #
    FORMAT = pyaudio.paInt16    #2 байта на сэмпл
    CHANNELS = 1                #каналы
    RATE = 44100                #частота дискретизации
    RECORD_SECONDS = 3          #длина записи
    lastId = 0                  #количество записанных wav фалов
    #samplesData = []            #хранение в памяти текущей записи
    byteData = b''

    def __init__(self):                         #дописать добавление записи в list
        voiceRec.lastId = voiceRec.lastId + 1
        self.id = voiceRec.lastId
        self.param1 = 0.0
        self.param2 = 0.0
        self.param3 = 0.0
        self.rec_done = False
        self.analyse_done = False

    def initWithParams(self, id, params1, params2, params3, rec_done, analyse_done):
        self.id = int(id)
        self.param1 = float(params1)
        self.param2 = float(params2)
        self.param3 = float(params3)
        self.rec_done = bool(int(rec_done))
        self.analyse_done = bool(int(analyse_done))
        if self.id > voiceRec.lastId:
            voiceRec.lastId = self.id

    def analyseRec(self):
        self.param1 += 1
        self.param2 += 2
        self.param3 += 3

    def recToRam(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        print("* recording")
        frames = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("* done recording")

        voiceRec.byteData = b''.join(frames)
        #voiceRec.samplesData = np.fromstring(byteData, dtype=np.int16)    #запись в статическую переменную
        #del byteData

        stream.stop_stream()
        stream.close()
        p.terminate()

#####################################################################################

    def noiseReduction (self, samples):
        for i in range(len(samples)-1):
            samples[i+1] = (samples[i+1] - 0.9 * samples[i])*(0.54 - 0.46 * np.cos((i+1-6)*2*np.pi/180))
        return samples


    def wavToRam(self):
        recNum = str(self.id)
        recNum = recNum.zfill(4)
        WAVE_INPUT_FILENAME = 'wavs/'+'voicerec_'+recNum+'.wav'
        wf = wave.open(WAVE_INPUT_FILENAME, 'rb')
        nframes = wf.getnframes()

        voiceRec.byteData = wf.readframes(nframes)
        #voiceRec.samplesData = np.fromstring(byteData, dtype=np.int16)  # запись в статическую переменную
        #del byteData
        wf.close()
        #print(voiceRec.samplesData)

    def playRam(self):
        self.wavToRam()
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        output=True)
        data = voiceRec.byteData
        stream.write(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def createWav(self):
        self.recToRam()
        recNum = str(self.id)
        recNum = recNum.zfill(4)
        print('номер записи в формате ХХХХ - ', recNum)
        print('номер записи в числовой форме - ', self.id)
        WAVE_OUTPUT_FILENAME = 'wavs/'+'voicerec_'+recNum+'.wav'
        
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(self.FORMAT))                              # было p.get_sample_size(FORMAT)
        wf.setframerate(self.RATE)
        samplesData = np.fromstring(voiceRec.byteData, dtype=np.int16)
        wf.writeframes(samplesData)
        wf.close()

        print(len(samplesData))
        #samples = voiceRec.samplesData

        #self.plotSignal(samples)
        #samples = self.noiseReduction(samples)
        #self.plotSignal(samples)
        #print(np.min(samples))
        #print(np.max(samples))
        #self.plotFFT(samples)

    def plotSignal(self):
        self.wavToRam()
        n = np.fromstring(self.byteData, dtype=np.int16)

        plt.figure(num='График сигнала')
        plt.plot(np.arange(len(n))/self.RATE, n)
        plt.xlabel('Время, c')
        plt.ylabel('Напряжение')
        plt.title('Сигнал')
        plt.grid(True)
        plt.show()

    def plotSignalSamples(self, samples):
        #n = np.fromstring(self.samplesData, dtype=np.int16)
        #plt.figure(num='График сигнала')
        plt.plot(np.arange(len(samples))/self.RATE, samples)
        plt.xlabel('Время, c')
        plt.ylabel('Характеристика')
        plt.title('Сигнал')
        plt.grid(True)
        plt.show()

    def analyseSignal(self):
        n = np.fromstring(self.byteData, dtype=np.int16)
        
        pass

    def plotFFT(self):
        n = np.fromstring(self.byteData, dtype=np.int16)
        ff = np.fft.rfft(n)
        # спектр
        # print(ff)
        plt.figure(num='Фурье до/после фильтра')
        plt.plot(np.fft.rfftfreq(len(n), 1./self.RATE), np.abs(ff)/(len(n)))
        freqs = np.fft.rfftfreq(len(n), 1./self.RATE)
        amps = np.abs(ff)/(len(n))

        # rfftfreq сделает всю работу по преобразованию номеров элементов массива в герцы
        # нас интересует только спектр амплитуд, поэтому используем abs из numpy (действует на массивы поэлементно)
        # делим на число элементов, чтобы амплитуды были в милливольтах, а не в суммах Фурье. 
        # Проверить просто — постоянные составляющие должны совпадать в сгенерированном сигнале и в спектре

        plt.xlabel('Частота, Гц')
        plt.ylabel('Преобладание')
        plt.title('Спектр')
        plt.grid(True)

        for i in range(len(ff)):            #фильтр
            if freqs[i] < 300:
                ff[i] = 0 + 0j

        plt.plot(np.fft.rfftfreq(len(n), 1./self.RATE), np.abs(ff)/(len(n)))
        plt.show()

################################################3

        #modifRec = np.fft.irfft(ff)
        #print('длина samples', len(n))
        #print('длина modif', len(modifRec))
        #self.plotSignalSamples(modifRec)
        #self.plotSignalSamples(n)

#########################################################################
        #bstr1 = "".encode()
        #for i in range(0, len(modifRec)):
        #    bstr1+=int(modifRec[i]).to_bytes(2, byteorder='little', signed = True)
        
        #wf = wave.open('modif.wav', 'wb')
        #wf.setnchannels(self.CHANNELS)
        #wf.setsampwidth(pyaudio.get_sample_size(self.FORMAT))
        #wf.setframerate(self.RATE)
        #wf.writeframes(bstr1)
        #wf.close()

############################################################################
"""         назад в строку samplesData
bstr = "".encode()
for i in range(0, len(n)):
    bstr+=int(n[i]).to_bytes(WIDTH, byteorder='little', signed = True)
"""


def loadDB():
    file = open("db.txt", 'r')
    voiceRecs = []
    while (1):
        line = file.readline()
        if line == "":
            break
        params = line.split()
        print("тип", type(params))
        print(params)
        tmp = voiceRec()
        tmp.initWithParams(params[0], params[1], params[2], params[3], params[4], params[5]) #сделать через args
        voiceRecs.append(tmp)
    print(voiceRecs[0].id)
    file.close()
    return voiceRecs

def saveDB(voiceRecs):
    file = open("db.txt", 'w')
    for i in range(len(voiceRecs)):
        string = ''
        string = string + str(voiceRecs[i].id) + ' ' + str(voiceRecs[i].param1) + \
                 ' ' + str(voiceRecs[i].param2) + ' ' + str(voiceRecs[i].param3) + \
                 ' ' + str(int(voiceRecs[i].rec_done)) + ' ' + str(int(voiceRecs[i].analyse_done))
        print(string)
        file.write(string + '\n')
    file.close()

