const WaveFile = require('wavefile').WaveFile

const writeFile = (samples) => {
  const wav = new WaveFile()
  
  wav.fromScratch(1, 44100, '16', samples)
  return Promise.resolve(wav.toBuffer())
}

module.exports = { writeFile }