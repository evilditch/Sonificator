import axios from 'axios'

const uploadFile = async (newFile) => {
  const data = new FormData()
  data.append('file', newFile)
  console.log('lähetettävä data', data)

  const response = await axios.post('/api', data)
  return response.data
}

export default { uploadFile }