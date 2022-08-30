const fileRouter = require('express').Router()
const readFile = require('../readFile')

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
    res.status(200).send(data.message)
  } catch(exception) {
    res.status(400).json({ error: exception.message })
    next(exception)
  }
})

module.exports = fileRouter