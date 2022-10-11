import numpy as np
import simpleaudio as sa
from datetime import date
from scipy.io import wavfile
from scipy import signal

class Sonification:
    # parameters:
    # data: None or array. If None, generate sine wave to data
    # duration: total duration of sonification in seconds
    # rate: sample rate
    # sound: sound type. 'sine', 'squared' or 'harmonic.
    # scale: max scale of given data, tupler. Is None, using min and max values of data.

    def __init__(self, data=None, duration=5, rate=48000, sound='sine', scale=None):
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
        self.sound = sound
        
        if scale is not None:
            self.scale = scale
        else:
            self.scale = (np.min(self.y), np.max(self.y))
                
        self.samples = self.generateSamples()
        
    def pitches(self):
        frequence = 120
        
        # scaling data with self.scale and between 0 to 6
        values = (self.y -self.scale[0]) / (self.scale[1] - self.scale[0]) * 5
        frequence *= 1.6**values
        return frequence

    def generateSamples(self):
        t = np.linspace(0, self.duration, int(self.duration * self.rate))
        frequences = np.repeat(self.pitches(), len(t)/len(self.y))

        if len(frequences) < len(t):
            frequences = np.append(frequences, np.zeros(len(t)-len(frequences)))

        print(len(frequences), len(t))

        phase = 0.0
        phaseResult = np.array([])

        for freq in frequences:
            phStep = 2 * np.pi * freq * 1/self.rate
            phase += phStep
            phaseResult = np.append(phaseResult, phase)

        sine = np.sin(phaseResult)

        if self.sound == 'sine':
            samples = sine
        elif self.sound == 'square':
            print(self.sound)
            samples = signal.square(2 * np.pi * 30 * t, duty=(sine + 1)/2)
            # samples = signal.square(2 * np.pi * t, duty=phaseResult)
        elif self.sound == 'harmonic':
            samples = sine + (0.2 * 2* sine) + (0.8 * 3 * sine) + (0.5 * 8 * sine)
        else:
            print('not supported sound type')
            return []
        
        return self.toInt16(samples)
        

    def getSineSamples(self, t, frequences):
        phase = 0.0
        phaseResult = np.array([])

        for freq in frequences:
            phStep = 2 * np.pi * freq * 1/self.rate
            phase += phStep
            phaseResult = np.append(phaseResult, phase)
            
        samples = np.sin(phaseResult)
        return samples
        
    def getSquareSamples(self, t, frequences):
        return scipy.signal.square(t, duty=frequences)

    def play(self):
        # sample = self.toInt16()
        
        play_obj = sa.play_buffer(self.samples, 1, 2, self.rate)

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

class Multisonification(Sonification):
    def __init__(self, *sonifications):
        self.sonifications = sonifications
        self.rate = self.checkRate()
        self.samples = self.mixSamples()

    def checkRate(self):
        for i in range(len(self.sonifications)-1):
            if self.sonifications[i].rate != self.sonifications[i+1].rate:
                raise Exception('All sonifications must have the same sample rate')

        return self.sonifications[0].rate

    def mixSamples(self):
        length = 0
        
        # looking for the longest sonification
        for sony in self.sonifications:
            if len(sony.samples) > length:
                length = len(sony.samples)

        # creating a list of sonification samples, adding zeros to end if length is less than longest length
        samples = []
        for sony in self.sonifications:
            samples.append(np.append(sony.samples, np.zeros(length - len(sony.samples))))
        
        mixedSamples = sum(samples)
        mixedSamples = mixedSamples * 0.1 / np.max(mixedSamples)
        
        return self.toInt16(mixedSamples)


class ScatterSonification(Sonification):
    def __init__(self, data=None, x=0, y=1, valuetime=0.02, scale=None):
        try:
            self.x = data[x]
            self.y = data[y]
        except BaseException as err:
            print('jokin meni vikaan')
            print(err)
            # raise Exeption('both x (time) and y (values) are required')
            if valuetime is None or isinstance(valuetime, float):
                self.valuetime = valuetime        
            else:
                raise Exception('Valuetime must be None or float (seconds)')
        # numpy.argsort(x) kertoo meille, mihin järjestykseen arvot pitää pistää
        Sonification.__init__(self, data, scale=scale)
        

    def generateSamples(self):
        x, y = self.sortXY()
        
        # timeX = np.linspace(np.min(x), np.max(x)+1, np.max(x))

        startTimes = self.getStartTimes(x)
        print('start times:', startTimes)

        yFrequences = self.pitches(y)
        print('frequences:', yFrequences)

        samples = map(self.getPlib, starttimes, yFrequences)

        # self.duration = self.valuetime * len(x)
            
        # scaling x between 0 to duration
        # x = (x - np.min(x)) / (np.max(x) - np.min(x)) * self.duration

         # that = np.linspace(0, self.duration, int(self.duration * self.rate))
        
        # yhden äänen pituus sampleina
        # oneSoundLen = len(t) /
        
        # index = 1
        
        # phase = 0.0
        # phaserResult = []

        # arr[i:i+len(plus)] = arr[i:i+len(plus)]+plus
        
        # while index <= len(t):
            
        
    def sortXY(self):
        i = np.argsort(self.x)
        return self.x[i], self.y[i]

    def getStartTimes(self, x):
        dx = abs(x[0] - x[-1])
        scale = float(dx) / float((self.duration * 1000))
        
        subtract = np.subtract(x[1:], x[0:-1])
        
        min = np.min(subtract[np.nonzero(subtract)])
        max = np.max(subtract)
        
        timeMin = min / scale
        timeMax = max / scale
        timeTotal = np.max(x) / scale

        durations = subtract / scale 
        startTimes = (x - np.min(x)) /         (scale * 1000) # in seconds

        return startTimes


    def pitches(self, y):
        frequence = 120
        
        # scaling data with self.scale and between 0 to 6
        values = (y -self.scale[0]) / (self.scale[1] - self.scale[0]) * 5
        frequence *= 1.6**values
        return frequence
