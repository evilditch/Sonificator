const fileRouter = require('express').Router()
const readFile = require('../readFile')
const audio = require('../generateAudio')
const writeWaveFile = require('../writeWaveFile')

fileRouter.post('/', async (req, res, next) => {
  if (!req.files) {
    return res.status(400).json({
      message: 'No file uploaded'
    })
  }

  const file = req.files.file
  console.log('saatiin', file)
  
  try {
    // tehdään tiedostolle jotain
    const data = await readFile.toArray(file)
    const wave = await audio.sampleA()
    const waveBuffer = await writeWaveFile.writeFile(wave)
    console.log(waveBuffer)

    res.status(200)
    res.set({
      'Cache-Control': 'no-cache',
      'Content-Type':  'audio/vnd.wav',
      'Content-Length': waveBuffer.length,
      'Content-Disposition': 'attachment; filename=audio.wav'
    })
    res.send(Buffer.from(waveBuffer))
  } catch(exception) {
    res.status(400).json({ error: exception.message })
    next(exception)
  }
})

module.exports = fileRouter