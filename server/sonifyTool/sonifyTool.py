import numpy as np
import simpleaudio as sa
from datetime import date
from scipy.io import wavfile

class Sonification:
    def __init__(self, data=None, duration=5, rate=48000):
        if data is not None:
            data = np.array(data)
            if data.ndim ==1:
                self.y = data
            else:
                print("Can't handle %s dimensional data yet" % data.ndim)
        else:
            self.x = np.linspace(0, 20, 200)
            self.y = np.sin(self.x)

        print(len(self.y))
        self.rate = rate # samples per seconds
        self.duration = duration #total duration in seconds
                
        self.samples = self.generateSamples()
        
    def pitches(self):
        frequence = 120
        frequence *= 1.6**self.y
        return frequence

    def generateSamples(self):
        t = np.linspace(0, self.duration, int(self.duration * self.rate))
        frequences = np.repeat(self.pitches(), len(t)/len(self.y))
        print(len(frequences), len(t))
        
        phase = 0.0
        phaseResult = np.array([])

        for freq in frequences:
            phStep = 2 * np.pi * freq * 1/self.rate
            phase += phStep
            phaseResult = np.append(phaseResult, phase)
            
        samples = np.sin(phaseResult)
        return self.toInt16(samples)
        

    def play(self):
        # sample = self.toInt16()
        
        play_obj = sa.play_buffer(self.samples, 2, 2, self.rate)

        # Wait for playback to finish before exiting
        play_obj.wait_done()
        return
            
            
    def toInt16(self, samples):
        # Ensure that highest value is in 16-bit range
        samples = samples * 32767 / np.max(np.abs(samples))

        # Convert to 16-bit data
        samples = samples.astype(np.int16)
    
        return samples

    def save(self, filename='sonification'+str(date.today())):
        filename = filename + '.wav'

        wavfile.write(filename, self.rate, self.samples)
        return