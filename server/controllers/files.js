const fileRouter = require('express').Router()

fileRouter.post('/', (req, res, next) => {
  const files = req.files
  console.log('saatiin', files)
  
  try {
    // tehdään tiedostolle jotain
    res.status(201).json({ message: `Saatiin tiedosto ${files.file.name}` })
  } catch(exception) {
    next(exception)
  }
})

module.exports = fileRouter