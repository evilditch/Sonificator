const fileRouter = require('express').Router()

fileRouter.post('/', (req, res, next) => {
  if (!req.files) {
    return res.send({
      status: false,
      message: 'No file uploaded'
    })
  }

  const file = req.files.file
  console.log('saatiin', file)
  
  try {
    // tehdään tiedostolle jotain
    res.status(200).json({ message: `Saatiin tiedosto ${file.name}` })
  } catch(exception) {
    next(exception)
  }
})

module.exports = fileRouter