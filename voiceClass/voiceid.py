
import pyaudio
import wave
import sys
import numpy as np  
import matplotlib.pyplot as plt  

class voiceRec:

    CHUNK = 1024
    FORMAT = pyaudio.paInt16    #2 байта на сэмпл
    CHANNELS = 1
    RATE = 44100                #частота дискретизации
    RECORD_SECONDS = 3          #
    RECORD_NUM = 0              #количество записанных wav фалов
    byteData = b''

    def __init__(self):
        self.param1 = 0
        self.param2 = 0
        self.param3 = 0

    def analyseRec(self):
        self.param1 += 1
        self.param2 += 2
        self.param3 += 3

    def recToRam(self):
        #####################################
        voiceRec.RECORD_NUM += 1
        #####################################
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
        
        voiceRec.byteData = b''.join(frames)  #запись в статическую переменную
        
        stream.stop_stream()
        stream.close()
        p.terminate()

#####################################################################################
        
    def createWav(self):
        self.recToRam()
        recNum = str(voiceRec.RECORD_NUM)
        recNum = recNum.zfill(4)
        print('номер записи в формате ХХХХ - ', recNum)
        print('номер записи в числовой форме - ', voiceRec.RECORD_NUM)
        WAVE_OUTPUT_FILENAME = 'voicerec_'+recNum+'.wav'
        
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(self.FORMAT))                              # было p.get_sample_size(FORMAT)
        wf.setframerate(self.RATE)
        wf.writeframes(voiceRec.byteData)
        wf.close()

        print(len(voiceRec.byteData))

        samples = np.fromstring(voiceRec.byteData, dtype=np.int16)
        self.plotSignal(samples)
        print(np.min(samples))
        print(np.max(samples))
        self.plotFFT(samples)

    def plotSignal(self, samples):
        plt.plot(np.arange(len(samples))/self.RATE, samples)                  # по оси времени секунды
        plt.xlabel('Время, c')                                      
        plt.ylabel('Напряжение, не мВ')
        plt.title('Сигнал')
        plt.grid(True)
        plt.show()

    def plotFFT(self, samples):

        ff = np.fft.rfft(samples)

        # спектр
        print(ff)
        plt.plot(np.fft.rfftfreq(len(samples), 1./self.RATE), np.abs(ff)/(len(samples)))

        freqs = np.fft.rfftfreq(len(samples), 1./self.RATE)
        amps = np.abs(ff)/(len(samples))
        # rfftfreq сделает всю работу по преобразованию номеров элементов массива в герцы
        # нас интересует только спектр амплитуд, поэтому используем abs из numpy (действует на массивы поэлементно)
        # делим на число элементов, чтобы амплитуды были в милливольтах, а не в суммах Фурье. 
        # Проверить просто — постоянные составляющие должны совпадать в сгенерированном сигнале и в спектре
        plt.xlabel('Частота, Гц')
        plt.ylabel('Напряжение, мВ')
        plt.title('Спектр')
        plt.grid(True)
        plt.show()


        for i in range(len(ff)):
            if freqs[i] < 300 :
                ff[i] = 0 + 0j


        plt.plot(np.fft.rfftfreq(len(samples), 1./self.RATE), np.abs(ff)/(len(samples)))
        plt.xlabel('Частота, Гц')
        plt.ylabel('Напряжение, мВ')
        plt.title('Спектр')
        plt.grid(True)
        plt.show()

#########################################################################
        modifRec = np.fft.irfft(ff)
        self.plotSignal(modifRec)
        self.plotSignal(samples)

#########################################################################
        bstr1 = "".encode()
        for i in range(0, len(modifRec)):
            bstr1+=int(modifRec[i]).to_bytes(2, byteorder='little', signed = True)

        p = pyaudio.PyAudio()
        wf = wave.open('modif.wav', 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(bstr1)
        wf.close()


############################################################################



"""
import pyaudio                                  #импорт библиотек для работы с аудио
import numpy as np                              #
from numpy.fft import rfft, rfftfreq            #
from math import sin, pi                        #
import matplotlib.pyplot as plt                 #



CHUNK = 1024            #размер буфера чтения/записи
WIDTH = 2               #размерность сэмпла, по 2 байта на каждый отсчет
CHANNELS = 1            #канал - 1
RATE = 44100            #частота дискретизации сигнала
RECORD_SECONDS = 5      #длительность записи сигнала

p = pyaudio.PyAudio()

print(p.get_default_input_device_info(),"\n") ##############################################

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)

print("* recording")

n = np.zeros(RATE*RECORD_SECONDS)

bstr1 = "".encode()

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):  #запись с микрофона в байтовую строку
    data = stream.read(CHUNK)
    bstr1 += data

print(bstr1[0:2])

for i in range(136):
    bstr1+=b'\x00\x00'

n = np.fromstring(bstr1, dtype=np.int16)

print (n[60000:61000])
"""

"""
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    
#    print (data,"\n")
#    stream.write(data, CHUNK)

print("\n", n[22000:23000], "\n")
"""

"""
bstr = "".encode()

#n = np.sort(n)

for i in range(0, int(RATE * RECORD_SECONDS - 500)):
    bstr+=int(n[i]).to_bytes(WIDTH, byteorder='little', signed = True)

print("из массива")
stream.write(bstr)

print("из строки")
stream.write(bstr1)

#print(n,"\n")
print("* done")

#for i in range(0, int(RATE * RECORD_SECONDS)):
 #   stream.write(n, i)




#print(ff,"\n")


 # нарисуем всё это, используя matplotlib

plt.plot(np.arange(88200)/44100, n) # по оси времени секунды!
plt.xlabel('Время, c') # это всё запускалось в Python 2.7, поэтому юникодовские строки
plt.ylabel('Напряжение, не мВ')
plt.title('Запись')
plt.grid(True)
plt.show()
# когда закроется этот график, откроется следующий

ff = rfft(n)
np.append(n, (np.zeros(7, dtype = np.complex)))

# Потом спектр
plt.plot(rfftfreq(RATE*RECORD_SECONDS, 1./RATE), np.abs(ff)/(RATE*RECORD_SECONDS))
# rfftfreq сделает всю работу по преобразованию номеров элементов массива в герцы
# нас интересует только спектр амплитуд, поэтому используем abs из numpy (действует на массивы поэлементно)
# делим на число элементов, чтобы амплитуды были в милливольтах, а не в суммах Фурье. 
# Проверить просто — постоянные составляющие должны совпадать в сгенерированном сигнале и в спектре
plt.xlabel('Частота, Гц')
plt.ylabel('Напряжение, мВ')
plt.title('Спектр')
plt.grid(True)
plt.show()


stream.stop_stream()
stream.close()

p.terminate()

"""
