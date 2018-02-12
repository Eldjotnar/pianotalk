# pianotalk
A nifty little python script for synthesizing speech on a piano

# running the script
pianotalk is written for python2.7 and requires [scipy](https://www.scipy.org/) and [mingus](https://github.com/bspaans/python-mingus) to run. Unfortunately, the output doesn't sound exactly like speech, but it is similar enough. When shown the words alongside the output, most people have been able to hear the words. Contributions are very welcome! If you have ideas about improving it, I'd love to work with you.

# How It Works
Fourier analysis shows that all sound can be represented as the sum of an infinite number of trigonometric functions. Audio (including speech samples) are naturally waves and can correspondingly be represented as a sum. Pianotalk works by taking the "Short Time Fast Fourier Transform" (STFFT) of the audio sample. You can watch the video that describes the science behind it here:
[![Explanation](http://img.youtube.com/vi/NaVkEvA0g-k/0.jpg)](http://www.youtube.com/watch?v=NaVkEvA0g-k)
