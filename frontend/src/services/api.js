/**
 * API Service Component
 * package all API calls in one place
 * provide unified interface for frontend to call backend APIs
 */
import axios from 'axios'

const baseURL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: '/api',  
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

export const processData = async ({ data, natural_language_input }) => {
  const response = await api.post('/process/', {
    data,
    natural_language_input,
  })
  
  return response.data
}

export default api
