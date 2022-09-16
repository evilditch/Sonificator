import numpy as np
import simpleaudio as sa

class Sonification:
    def __init__(self):
        self.x = np.linspace(0, 5, 100)
        self.y = np.sin(self.x)
        print(len(self.y))
        self.fs = 48000 # samples per seconds
        self.duration = 5 #total duration in seconds
        
        t = np.linspace(0, self.duration, int(self.duration*self.fs))
        frequences = np.repeat(self.pitches(), len(t)/len(self.y))
        print(len(frequences), len(t))
        
        self.sample = np.sin(2 * np.pi * t * frequences)
        
    def pitches(self):
        frequence = 120
        frequence *= 1.6**self.y
        return frequence

    def play(self):
        sample = self.toInt16()
        
        play_obj = sa.play_buffer(sample, 2, 2, self.fs)

        # Wait for playback to finish before exiting
        play_obj.wait_done()
        return
            
            
    def toInt16(self):
        # Ensure that highest value is in 16-bit range
        sample = self.sample * 32767 / np.max(np.abs(self.sample))

        # Convert to 16-bit data
        sample = sample.astype(np.int16)
    
        return sample
