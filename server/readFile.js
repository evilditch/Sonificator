const fs = require('fs')
const { parse } = require('csv-parse')

const parseFile = (file) => {
  // check that the file type is accepted (.csv or .tsv), and choose correct delimiter
  const fileType = file.name.split('.')[1]
  let delimiter = ''

  if (fileType === 'csv') {
    console.log('csv-tiedosto')
    delimiter = ','
    // const data = { message: `saatiin csv-tiedosto ${file.name}`}
    // return Promise.resolve(JSON.stringify(data))
  } else if (fileType === 'tsv') {
    console.log('tsv-tiedosto')
    delimiter = '\t'
    // const data = { message: `saatiin tsv-tiedosto ${file.name}`}
    // return Promise.resolve(JSON.stringify(data))
  } else {
    console.log('jotain muuta', fileType)
    const err = { message: `File must be .csv or .tsv, it was .${fileType}`}
    return Promise.reject(err)
  }

  // eka yritys tiedoston lukemiseen ei toiminut
  // fs.createReadStream(file.data)
  //   .pipe(parse({ delimiter: delimiter }))
  //   .on("data", (row) => {
  //     console.log(row)
  //   })
  //   .on("error", (error) => {
  //     console.log(error)
  //     return Promise.reject(error)
  //   })
    return Promise.resolve(JSON.stringify({ message: 'tiedosto luettiin' }))
}

module.exports = { parseFile }