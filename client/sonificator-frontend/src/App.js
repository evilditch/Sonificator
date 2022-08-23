import FileForm from './components/FileForm'

const App = () => {
  
  const file = (filename) => {
    console.log(filename)
  }

  return (
    <>
      <h1>Sonificator</h1>
      <FileForm handleFile={file} />
    </>
  )
}

export default App