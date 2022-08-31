const fs = require('fs')
const { parse } = require('csv-parse')

const toArray = (file) => {
  console.log(file.data.toString())
  
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

  const dataStr = file.data.toString()

  // Split data string to array of rows
  const rows = dataStr.slice(dataStr.indexOf('\n') + 1).split('\n')

  // If the last row in file are empty, remove it from array
  if (rows[rows.length-1] === '') {
    rows.pop()
  }

  // Split row strings by delimiter and parse value to float number -> each rows are arrays
  const rowsArray = rows.map(row => row.split(delimiter).map(value => parseFloat(value)))

  // transposing array to columns -> each array has values of one variable
  const transpose = (matrix) => {
    return matrix[0].map((col, i) => matrix.map(row => row[i]))
  }
  
  const data = transpose(rowsArray)
  console.log(data)

  return Promise.resolve({ data: data, message: 'tiedosto luettiin' })
}

module.exports = { toArray }