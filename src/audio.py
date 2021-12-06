import struct

import pyaudio
from scipy import optimize

import numpy as np

def exponentFun(x, x0, y0, k):
    return -k*(x-x0)**2+y0

def findPeak(f,Pxx):
    i_max = Pxx.argmax(axis=0)
    if i_max > 5:
        try:
            fR = f[i_max - 1:i_max + 2]
            PR = Pxx[i_max - 1:i_max + 2]
            popt, _ = optimize.curve_fit(exponentFun, fR, PR)  # začetna funkcija, x,y
            x2 = np.linspace(fR[0], fR[-1], 50)
            y2 = exponentFun(x2, *popt)

            M = y2.argmax(axis=0)

            return x2[M],x2,y2
        except Exception:
            pass
    return None

FORMAT = pyaudio.paInt16
RATE = 44100
CHANNELS = 2

# Set Plot Range [-RANGE,RANGE], default is nyquist/2
RANGE = RATE/2

# Set these parameters (How much data to plot per FFT)
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

# Which Channel? (L or R)
LR = "l"
class Audio():
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.initMicrophone()

    def initMicrophone(self):
        device_index = self.find_input_device()

        self.stream = self.pa.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   input=True,
                                   input_device_index=device_index,
                                   frames_per_buffer=INPUT_FRAMES_PER_BLOCK)
    def find_input_device(self):
        device_index = None
        for i in range(self.pa.get_device_count()):
            devinfo = self.pa.get_device_info_by_index(i)
            if devinfo["name"].lower() in ["mic","input"]:
                device_index = i

        return device_index
    def readData(self):
        block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        count = len(block)/2
        format = "%dh"%(count)
        shorts = struct.unpack( format, block )
        if CHANNELS == 1:
            return np.array(shorts)
        else:
            l = shorts[::2]
            r = shorts[1::2]
            if LR == 'l':
                return np.array(l)
            else:
                return np.array(r)

    def get_spectrum(self, data):
        T = 1.0 / RATE
        N = data.shape[0]
        Pxx = (1. / N) * np.fft.fft(data)
        f = np.fft.fftfreq(N, T)
        Pxx = np.fft.fftshift(Pxx)
        f = np.fft.fftshift(f)

        Pxx = Pxx[len(Pxx) // 2:]
        f = f[len(f) // 2:]

        return f, (np.absolute(Pxx))
