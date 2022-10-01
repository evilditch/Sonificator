import numpy as np
import simpleaudio as sa

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
        
        # t = np.linspace(0, self.duration, int(self.duration*self.rate))
        # frequences = np.repeat(self.pitches(), len(t)/len(self.y))
        # print(len(frequences), len(t))
        
        # self.samples = np.sin(2 * np.pi * t * frequences)
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
        return samples
        

    def play(self):
        sample = self.toInt16()
        
        play_obj = sa.play_buffer(sample, 2, 2, self.rate)

        # Wait for playback to finish before exiting
        play_obj.wait_done()
        return
            
            
    def toInt16(self):
        # Ensure that highest value is in 16-bit range
        sample = self.samples * 32767 / np.max(np.abs(self.samples))

        # Convert to 16-bit data
        sample = sample.astype(np.int16)
    
        return sample
