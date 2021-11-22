import struct

import numpy as np
import pyaudio
import wave
import sys

from pyqtgraph.Qt import QtGui
from scipy.fft import fft


class AudioFile:
    chunk = 1024

    def __init__(self,curve):
        # stream constants
        self.curve=curve
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.pause = False

        # stream object
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.chunk,
        )

    def play(self):
        """ Play entire file """

        while True:
            data = self.stream.read(self.chunk)
            y = self.getSpecter(data)
            ##self.curve.setData(y)

            #self.curve.setPos()

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()

    def getSpecter(self, data):

        # data_int = struct.unpack(str(2 * self.chunk) + 'B', data)
        # data_np = np.array(data_int, dtype='b')[::2] + 128
        # # compute FFT and update line
        # yf = fft(data_int)
        # y = np.abs(yf[0:self.chunk]) / (128 * self.chunk)

        data = ((data / np.power(2.0, 15)) * 5.25)

        # compute FFT parameters
        f_vec = self.RATE * np.arange(self.chunk / 2) / self.chunk  # frequency vector based on window size and sample rate
        mic_low_freq = 100
        low_freq_loc = np.argmin(np.abs(f_vec - mic_low_freq))
        fft_data = (np.abs(np.fft.fft(data))[0: int(np.floor(self.chunk / 2))]) / self.chunk
        fft_data[1:] = 2 * fft_data[1:]

        max_loc = np.argmax(fft_data[low_freq_loc:]) + low_freq_loc
        print(max_loc)
        return max_loc
#
#     # Usage example for pyaudio
# a = AudioFile()
# a.play()
# a.close()
#
# p.terminate()

