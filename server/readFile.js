const fs = require('fs')
const { parse } = require('csv-parse')

const parseFile = (file) => {
  const fileType = file.name.split('.')[1]
  if (fileType === 'csv') {
    console.log('csv-tiedosto')
    const data = { message: `saatiin csv-tiedosto ${file.name}`}
    return Promise.resolve(JSON.stringify(data))
  } else if (fileType === 'tsv') {
    console.log('tsv-tiedosto')
    const data = { message: `saatiin tsv-tiedosto ${file.name}`}
    return Promise.resolve(JSON.stringify(data))
  } else {
    console.log('jotain muuta', fileType)
    const err = { message: `väärä tiedostomuoto ${file.name}`}
    return Promise.reject(err)
  }
  // fs.createReadStream(file)
  
}

module.exports = { parseFile }