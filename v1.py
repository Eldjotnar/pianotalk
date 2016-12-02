import numpy as np 
import matplotlib.pyplot as plt
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fftpack, arange, fft
from scipy.io import wavfile
import scipy.fftpack

from mingus.containers import Note

THRES = 1
INPUT_FILE = '440_square_long.wav'
WINDOW_LEN = 0.01 #ms (10ms is default)

#return frequencies above a threshold
def getFrequencies(y, Fs):
	#compute fft and frequencies
	n = len(y)
	Y = fft(y)/n
	find_freqs = scipy.fftpack.fftfreq(n)
	
	freqs = []
	vol = []
	#pick out the frequencies above the threshold
	max = np.argmax(np.abs(Y))
 	for i in range(0,n):
 		if abs(Y[i]) > THRES:
 			freqs.append(abs(find_freqs[i]*Fs))
 			vol.append(scale(abs(Y[i]),THRES,max))
 			#print("vol is " + str(vol[-1]))
 			#print(abs(find_freqs[i]*Fs)) #freqeuncies in Hz
 	#print("There are " + str(len(freqs)))

#scales a value between 1 and 127
def scale(x, min, max):
 	return (127 * (x - min))/(max - min) + 1

def main():
	#read in audio and select channel
	Fs, data = wavfile.read(INPUT_FILE)
	y = data[:,0]

	#pass a window over small amount of the sound file with overlap
	sampSize = (Fs * WINDOW_LEN)/2
	prevStart = 0
	end = int(sampSize)
	totalSamp = (len(y)/(sampSize*2) *2) #number of times to loop

	#iterate over the data
	for j in range(0,totalSamp):
		#print("Getting frequencies between " + str(prevStart/Fs) + " and " + str(end/Fs))
		#print("Getting frequencies between " + str(prevStart) + " and " + str(end))
		getFrequencies(y[prevStart:end],Fs)
		prevStart += sampSize
		end += sampSize

	#print(sampSize)

	#plot the incoming audio signal
	subplot(2,1,1)
	plot(data[:1000])
	xlabel('Time')
	ylabel('Amplitude')

	#plot the power spectrum
	subplot(2,1,2)
	#getFrequencies(y,Fs)
	show()

if __name__ == '__main__':
  main()