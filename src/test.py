#!/usr/bin/python

"""
PyAudio + PyQtGraph Spectrum Analyzer

Author:@sbarratt
Date Created: August 8, 2015

"""

import pyaudio
import struct
import math

from astropy import modeling
from matplotlib import pyplot as plt
from pyqtgraph import mkPen
from scipy import optimize
import sys
import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

# Audio Format (check Audio MIDI Setup if on Mac)
FORMAT = pyaudio.paInt16
RATE = 44100
CHANNELS = 2

# Set Plot Range [-RANGE,RANGE], default is nyquist/2
RANGE = None
if not RANGE:
    RANGE = RATE/2

# Set these parameters (How much data to plot per FFT)
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

# Which Channel? (L or R)
LR = "l"

def gaussian(x, x0, y0, k):
    return -k*(x-x0)**2+y0

class SpectrumAnalyzer():
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.initMicrophone()
        self.initUI()

    def find_input_device(self):
        device_index = None
        for i in range(self.pa.get_device_count()):
            devinfo = self.pa.get_device_info_by_index(i)
            if devinfo["name"].lower() in ["mic","input"]:
                device_index = i

        return device_index

    def initMicrophone(self):
        device_index = self.find_input_device()

        self.stream = self.pa.open(	format = FORMAT,
                                       channels = CHANNELS,
                                       rate = RATE,
                                       input = True,
                                       input_device_index = device_index,
                                       frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

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

    def initUI(self):
        self.app = QtGui.QApplication([])
        self.app.quitOnLastWindowClosed()

        self.mainWindow = QtGui.QMainWindow()
        self.mainWindow.setWindowTitle("Spectrum Analyzer")
        self.mainWindow.resize(800,300)
        self.centralWid = QtGui.QWidget()
        self.mainWindow.setCentralWidget(self.centralWid)
        self.lay = QtGui.QVBoxLayout()
        self.centralWid.setLayout(self.lay)

        self.specWid = pg.PlotWidget(name="spectrum")
        self.fitItem = self.specWid.getPlotItem()
        self.specItem = self.specWid.getPlotItem()
        self.specItem.setMouseEnabled(y=False)
        self.specItem.setYRange(0,1000)
        self.specItem.setXRange(1000, 2000, padding=0)

        self.specAxis = self.specItem.getAxis("bottom")
        self.specAxis.setLabel("Frequency [Hz]")
        self.lay.addWidget(self.specWid)

        self.mainWindow.show()
        self.app.aboutToQuit.connect(self.close)

    def close(self):
        self.stream.close()
        sys.exit()

    def get_spectrum(self, data):
        T = 1.0/RATE
        N = data.shape[0]
        Pxx = (1./N)*np.fft.fft(data)
        f = np.fft.fftfreq(N,T)
        Pxx = np.fft.fftshift(Pxx)
        f = np.fft.fftshift(f)

        Pxx = Pxx[len(Pxx)//2:]
        f = f[len(f)//2:]

        return f, (np.absolute(Pxx))

    def mainLoop(self):
        while 1:
            # Sometimes Input overflowed because of mouse events, ignore this
            try:
                data = self.readData()
            except IOError:
                continue
            f, Pxx = self.get_spectrum(data)

            i_max = Pxx.argmax(axis=0)

            if i_max > 5:
                try:
                    fR = f[i_max-1:i_max+2]
                    PR = Pxx[i_max-1:i_max+2]
                    popt, _ = optimize.curve_fit(gaussian, fR, PR)
                    x2 = np.linspace(fR[0], fR[-1], 10)
                    y2 = gaussian(x2, *popt)

                    M = y2.argmax(axis=0)
                    print(x2[M], f[i_max])
                    self.fitItem.plot(x=x2,y=y2, clear=True, pen=mkPen('r', width=3))
                except Exception:
                    pass

            self.specItem.plot(x=f,y=Pxx, clear=False)
            QtGui.QApplication.processEvents()

if __name__ == '__main__':
    sa = SpectrumAnalyzer()
    sa.mainLoop()
