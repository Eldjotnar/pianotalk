# pianotalk
A nifty little python script for synthesizing speech on a piano

pianotalk is written for python2.7 and requires scipy and mingus to run successfully. The output doesn't sound exactly like speech, but it is similar enough. When shown the words alongside the output, most people have been able to hear the words.

#How It Works
Fourier analysis shows that all sound can be represented as the sum of an infinite number of trigonometric functions. Audio (including speech samples) are naturally waves and can correspondingly be represented as a sum. Pianotalk works by taking the "Short Time Fast Fourier Transform" (STFFT) of the audio sample.
