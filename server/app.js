const config = require('./utils/config')
const express = require('express')

const app = express()

const fileUpload = require('express-fileupload')
const cors = require('cors')
const logger = require('./utils/logger')
const fileRouter = require('./controllers/files')

app.use(fileUpload({
  createParentPath: true
}))

app.use(cors())
app.use(express.json())

app.get('/info', (req, res, next) => {
  res.send(`<p>Sonificator-palvelin vastaa täällä.</br> ${new Date()}</p>`)
})

app.use('/api', fileRouter)

const unknownEndpoint = (req, res) => {
  res.status(404).send({ error: 'Unknown endpoint' })
}

app.use(unknownEndpoint)

const errorHandler = (err, req, res, next) => {
  logger.error(err.message)

  next(err)
}

app.use(errorHandler)


module.exports = app
