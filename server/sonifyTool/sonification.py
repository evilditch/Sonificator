import numpy as np
import simpleaudio as sa
from datetime import date
from scipy.io import wavfile
from scipy import signal
from sklearn.linear_model import LinearRegression

def findIndex(x, xs):
    # Find the index corresponding to a given value in an array.
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n - 1) * (x - start) / (end - start))
    return int(i)


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
        
        if sound == 'sine':
            self.func = np.sin
        elif sound == 'cos':
            self.func = np.cos
        elif sound == 'sinc':
            self.func = np.sinc
        elif sound == 'square':
            self.func = self.squareSamples
        elif sound== 'saw':
            self.func = self.sawtoothSamples
        elif sound == 'triangle':
            self.func = self.triangleSamples
        else:
            print("Dont supported sound type {}. Using 'sine'".format(sound))
            self.func = np.sin

        self.samples = self.generateSamples()
        
    def pitches(self):
        frequence = 120
        
        # scaling data with self.scale and between 0 to 6
        values = (self.y -self.scale[0]) / (self.scale[1] - self.scale[0]) * 3.5
        # values = self.y
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

        # sine = np.sin(phaseResult)
        #
        # if self.sound == 'sine':
        #     samples = sine
        # elif self.sound == 'square':
        #     print(self.sound)
        #     samples = signal.square(2 * np.pi * 30 * t, duty=(sine + 1)/2)
        #     # samples = signal.square(2 * np.pi * t, duty=phaseResult)
        # elif self.sound == 'harmonic':
        #     samples = sine + (0.2 * 2* sine) + (0.8 * 3 * sine) + (0.5 * 8 * sine)
        # else:
        #     print('not supported sound type')
        #     return []
        
        samples = self.func(phaseResult)
        
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
        
    def squareSamples(self, phases):
        t = np.linspace(0, self.duration, int(self.duration * self.rate))
        return  0.001 * signal.square(2 * np.pi * 30 * t, duty=(np.sin(phases) + 1)/2)

    def sawtoothSamples(self, phases):
        # t = np.linspace(0, self.duration, int(self.duration * self.rate))
        return signal.sawtooth(2 * np.pi * phases)

    def triangleSamples(self, phases):
        return signal.sawtooth(2 * np.pi * phases, width=0.5)

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

class Line(Sonification):
    def __init__(self, data=None, duration=5, rate=48000, sound='sine', scale=None):
        Sonification.__init__(self, data, scale=scale, duration=duration, sound=sound)

    def generateSamples(self):
        frequences = self.pitches()
        
        phase = 0.0
        phaseResult = np.array([])

        for freq in frequences:
            phStep = 2 * np.pi * freq * 1/self.rate
            phase += phStep
            phaseResult = np.append(phaseResult, phase)

        # sine = np.sin(phaseResult)
        #
        # if self.sound == 'sine':
        #     samples = sine
        # elif self.sound == 'square':
        #     print(self.sound)
        #     samples = signal.square(2 * np.pi * 30 * t, duty=(sine + 1)/2)
        #     # samples = signal.square(2 * np.pi * t, duty=phaseResult)
        # elif self.sound == 'harmonic':
        #     samples = sine + (0.2 * 2* sine) + (0.8 * 3 * sine) + (0.5 * 8 * sine)
        # else:
        #     print('not supported sound type')
        #     return []

        samples = self.func(phaseResult)

        return self.toInt16(samples)
        

    def pitches(self):
        frequences = super().pitches()

        n = round((self.duration * self.rate) / (len(frequences) -1)) 
        print(n)
        linearFrequences = np.array([])
        
        for i in range(len(frequences) - 1):
            linearFrequences = np.append(linearFrequences, np.linspace(frequences[i], frequences[i+1], n, endpoint=False))
            # print(len(linearFrequences))
            
        linearFrequences = np.append(linearFrequences, frequences[-1])
        print(self.duration*self.rate, len(linearFrequences))
        return linearFrequences

class ScatterSonification(Sonification):
    def __init__(self, data=None, x=0, y=1, plibtime=0.1, scale=None, duration=5, sound='sine'):
        try:
            self.x = np.asarray(data[x])
            self.y = np.asarray(data[y])
        except BaseException as err:
            print('jokin meni vikaan')
            print(err)
            # raise Exeption('both x (time) and y (values) are required')
        self.plibtime = plibtime        
        # numpy.argsort(x) kertoo meille, mihin järjestykseen arvot pitää pistää
        Sonification.__init__(self, data, scale=scale, duration=duration, sound=sound)
        

    def generateSamples(self):
        x, y = self.sortXY()
        
        # timeX = np.linspace(np.min(x), np.max(x)+1, np.max(x))

        startTimes = self.getStartTimes(x)
        print('start times:', startTimes)

        yFrequences = self.pitches(y)
        print('frequences:', yFrequences)

        plibs = map(self.makePlib, startTimes, yFrequences)

        sumPlibs = sum(plibs)
        samples = sumPlibs.samples
        
        return self.toInt16(samples)

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

    def makePlib(self, startTime, frequency):
        # luodaan yksi yksittäinen ääni. t alkaa äänen aloitushetkestä.

        n = round(self.plibtime * self.rate)
        t = startTime + np.arange(n) / self.rate
        
        phases = 2 * np.pi * frequency * t
        
        samples = self.func(phases)
        return Plib(samples, t=t, rate=self.rate)

class Plib:
    def __init__(self, samples, t=None, rate=48000):
        self.samples = np.asarray(samples)
        self.rate = rate
        if t is not None:
            self.t = np.asarray(t)
        else:
            self.t = np.arange(len(samples)) / self.rate

    @property
    def start(self):
        return self.t[0]
        
    @property
    def end(self):
        return self.t[-1]
        
    def __add__(self, other):
        if other == 0:
            return self

        if self.rate != other.rate:
            raise Exception('sample rate must be same')

        start = min(self.start, other.start)
        end = max(self.end, other.end)
        n = int(round((end - start) * self.rate)) + 1
        samples = np.zeros(n)
        t = start + np.arange(n) / self.rate
        
        def addPlib(plib):
            i = findIndex(plib.start, t)
            
            j = i + len(plib.samples)
            samples[i:j] += plib.samples

        addPlib(self)
        addPlib(other)
        
        return Plib(samples, t, self.rate)
        
    __radd__ = __add__
    
class RegplotSonification(Multisonification):
    # yhdistetään 'scatterplot' ja datasta laskettu 'trendline' 
    
    def __init__(self, x=0, y=1, data=None, scale=None, sound='sine', rate=480000, duration=5, plibtime=0.1):
        self.duration = duration
        self.rate = rate
        self.scale = scale
        self.sound = sound

        self.scatter = ScatterSonification(data=data, x=x, y=y, scale=scale, duration=duration, sound=sound, plibtime=plibtime)
        self.x, self.y = self.scatter.sortXY()

        self.line = self.trendline()

        Multisonification.__init__(self, self.scatter, self.line)

    def trendline(self):
        trend = LinearRegression().fit(self.x.reshape(-1, 1), self.y)
        trendLine = trend.predict(self.x.reshape(-1, 1))
        
        return Line(data=trendLine, scale=self.scale, duration=self.duration, sound=self.sound, rate=self.rate)
        
    def playScatter(self):
        self.scatter.play()
        
    def playTrendline(self):
        self.line.play()
