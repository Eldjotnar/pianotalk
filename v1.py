import numpy as np 
import matplotlib.pyplot as plt
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fftpack, arange, fft
from scipy.io import wavfile
import scipy.fftpack

THRES = 1
INPUT_FILE = '440_sine_clean.wav'

#return frequencies above a threshold
def getFrequencies(y, Fs):
	#compute fft and frequencies
	Y = fft(y)/n
	n = len(y)
	freqs = scipy.fftpack.fftfreq(n)
	
	#pick out the frequencies above the threshold
	idx = np.argmax(np.abs(Y))
 	for i in range(0,n):
 		if abs(Y[i]) > THRES:
 			print(abs(freqs[i]*Fs))

def main():
	#read in audio and select channel
	Fs, data = wavfile.read(INPUT_FILE)
	y = data[:,0]

	#plot the incoming audio signal
	subplot(2,1,1)
	plot(data)
	xlabel('Time')
	ylabel('Amplitude')

	#plot the power spectrum
	subplot(2,1,2)
	getFrequencies(y,Fs)
	show()

if __name__ == '__main__':
  main()