import os

import numpy as np
import time
import heapq

from scipy.fft import fft
from scipy.io import wavfile
import scipy.fftpack

from mingus.containers import Note, NoteContainer
from mingus.midi import fluidsynth

#initialize global constants
INPUT_FILE = 'audio/gus_3.wav'
WINDOW_LEN = 0.01
PLAYBACK = 0.0034
BAR = []

#returns chord of dominant frequencies with associated volume
def getFrequencies(y, Fs):
    n = len(y)
    Y = fft(y)/n
    find_freqs = scipy.fftpack.fftfreq(n)
    
    freqs = []
    vol = []
    top_freqencies = heapq.nlargest(50,Y)
    maxi = max(np.abs(Y)**2)
    mini = min(np.abs(Y)**2)

    for i in range(0,n):
        if Y[i] in top_freqencies:
            freqs.append(abs(find_freqs[i]*Fs))
            vol.append(scale(abs(Y[i])**2,mini,maxi))
    assert len(freqs) == len(vol)
    createChord(freqs,vol)

#scales a value between 1 and 127
def scale(x, min, max):
     return int(round(115 * (x - min))/(max - min))

#creates a mingus chord out of each frequency with assoc. volume
def createChord(freqList = [], volList = []):
    chord = NoteContainer()
    for i in range(0,len(freqList)):
        sel_freq = freqList[i]
        #scale the volumes of present frequencies
        if(sel_freq > 27 and sel_freq < 4186):
            new_Note = Note().from_hertz(sel_freq,440)
            if(sel_freq < 220 or sel_freq > 2500):
                if(sel_freq < 100 or sel_freq > 3000):
                    volList[i] /= 1.4
                else:
                    volList[i] /= 1.2
            new_Note.velocity = volList[i]
            if(len(BAR) > 0):
                #don't play repeat notes as quickly
                if not new_Note in (BAR[-1]):
                    chord.add_note(new_Note)
    BAR.append(chord)

#applies a smoothing function to the input signal
def smooth(x,window_len=11,window='blackman'):
    s = np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    w = eval('np.'+window+'(window_len)')
    y = np.convolve(w/w.sum(),s,mode='valid')
    return y
    
def main():
    #take first channel of file    
    Fs, data = wavfile.read(INPUT_FILE)
    y = data[:,0]

    #load piano soundfont
    SF2 = os.path.expanduser('~/roaming_linux_daniel/soundfonts/Yamaha-Grand-Lite-v2.0.sf2')
    if not fluidsynth.init(SF2):
        print ("Couldn't load soundfont", SF2)
    
    #initialize variables for windowing
    sampSize = round((Fs * WINDOW_LEN)/2)
    prevStart = 0
    end = int(sampSize)
    totalSamp = int(len(y)/(sampSize*2) *2)

    #get the chords of the smoothed input
    for j in range(0,totalSamp):
        getFrequencies(smooth(y[prevStart:end]),Fs)
        prevStart += sampSize
        end += sampSize

    #play the chord back out again
    for idx,chord in enumerate(BAR):
        fluidsynth.play_NoteContainer(chord)
        time.sleep(PLAYBACK)
    time.sleep(PLAYBACK+0.3)
    
if __name__=='__main__':
    # print("Playing Sine Wave Synthesis")
    # call(["afplay","audio/sws.wav"])
    # print("Playing Sample Audio")
    # call(["afplay","audio/knife.wav"])
    # print("Playing SWS again")
    # call(["afplay","audio/sws.wav"])
    # print("Playing original again")
    # call(["afplay","audio/knife.wav"])
    print("Playing Piano Version")
    main()
