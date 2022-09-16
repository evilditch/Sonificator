
const sampleRate = 44100 // hz

// create array values from 0 to sound length in seconds, the length of this array is seconds*sampleRate
const timePoints = (seconds) => {
  const arr = []
  const step = seconds / (seconds * sampleRate -1)

  for (i = 0; i<seconds*sampleRate; i++) {
    arr.push(i*step)
  }
  
  return arr
}

const sampleA = () => {
  const frequency = 261.626
  const t = timePoints(2)

  const wave = Math.sin(2 * Math.PI * frequency * t)
  
  return Promise.resolve(wave)
}

module.exports = { sampleA }