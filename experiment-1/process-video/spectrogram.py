import argparse
import scipy.io.wavfile as wavfile
import scipy.signal as signal
import matplotlib.pyplot as plt
import numpy

def spectrogram(filename):
  rate, data = wavfile.read(filename)

  f, t, Sxx = signal.spectrogram(partial_data, fs=11025)
  return Sxx

#  plt.pcolormesh(t, f, Sxx)
#  plt.yscale('log')
#  plt.axis([0, 5, 1, 11025/2])
#  plt.ylabel('Frequency [Hz]')
#  plt.xlabel('Time [sec]')
#  plt.show()
