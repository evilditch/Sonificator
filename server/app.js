const config = require('./utils/config')
const express = require('express')

const app = express()

// ehkä tarvitaan cors, se tulisi tähän

const logger = require('./utils/logger')

app.use(express.json())

app.get('/info', (req, res, next) => {
  res.send(`<p>Sonificator-palvelin vastaa täällä.</br> ${new Date()}</p>`)
})

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
