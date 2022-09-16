const WaveFile = require('wavefile').WaveFile
const fs = require('fs/promises')

const writeFile = async (samples) => {
  let wav = new WaveFile()
  
  wav.fromScratch(1, 44100, '16', samples)

  const filePath = './exampleData/sonification.wav'
  
  await fs.writeFile(filePath, wav.toBuffer())
  return Promise.resolve(fs.readFile(filePath))
}

module.exports = { writeFile }