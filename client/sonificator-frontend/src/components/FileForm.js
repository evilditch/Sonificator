import { useState } from 'react'
import React from 'react'

const FileForm = ({ handleFile }) => {
  const fileInput = React.createRef()

  const handleSubmit = (event) => {
    event.preventDefault()
    handleFile(fileInput.current.files[0])
  }

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor='file'>Valitse tiedosto (.csv tai .tsv)</label>
      <input type='file' id='file' ref={fileInput} accept='.csv,.tsv' />
      <button type='submit'>Lähetä</button>
    </form>
  )
}

export default FileForm