import FileForm from './components/FileForm'
import fileService from './services/files'

const App = () => {
  
  const file = async (newFile) => {
    console.log(newFile)
    try {
      const response = await fileService.uploadFile(newFile)
      console.log(response)
    } catch(exception) {
      console.log('jokin meni pieleen', exception)
    }
  }

  return (
    <>
      <h1>Sonificator</h1>
      <FileForm handleFile={file} />
    </>
  )
}

export default App