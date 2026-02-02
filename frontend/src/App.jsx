/**
 * Main App Component
 * combines all major components and manages application state
 * the main entry point of the frontend application
 */
import React, { useState } from 'react'
import FileUpload from './components/FileUpload'
import DataTable from './components/DataTable'
import PatternInput from './components/PatternInput'
import ResultDisplay from './components/ResultDisplay'
import { processData } from './services/api'
import './App.css'

const App = () => {
  const [fileData, setFileData] = useState(null)
  
  const [columns, setColumns] = useState([])
  
  const [isProcessing, setIsProcessing] = useState(false)
  
  const [result, setResult] = useState(null)
  
  const [error, setError] = useState(null)

  const handleUploadSuccess = (response) => {
    setFileData(response.data)
    setColumns(response.columns)
    setResult(null)
    setError(null)
  }

  const handleUploadError = (errorMsg) => {
    setError(errorMsg)
    setFileData(null)
    setColumns([])
  }

  const handleProcess = async (params) => {
    if (!fileData || fileData.length === 0) {
      setError('Please upload a file before processing.')
      return
    }

    setIsProcessing(true)
    setError(null)

    try {
      const response = await processData({
        data: fileData,
        natural_language_input: params.natural_language_input,
      })
      setResult(response)
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'Data processing failed.'
      setError(errorMsg)
      setResult(null)
    } finally {
      setIsProcessing(false)
    }
  }

  const handleDownload = (data) => {
    if (!data || data.length === 0) {
      alert('No data available for download.')
      return
    }

    const headers = Object.keys(data[0])
  
    const csvContent = [
      headers.join(','),
      ...data.map(row => 
        headers.map(header => {
          const value = row[header] || ''

          return `"${String(value).replace(/"/g, '""')}"`
        }).join(',')
      )
    ].join('\n')

    const BOM = '\uFEFF'
    const blob = new Blob([BOM + csvContent], { 
      type: 'text/csv;charset=utf-8;' 
    })
    
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', 'processed_data.csv')
    link.style.visibility = 'hidden'
    
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    
    URL.revokeObjectURL(url)
  }

  return (
    <div className="app">
      <div className="container">
        <header className="app-header">
          <h1>Regular expression pattern matching tool</h1>
          <p>Upload CSV/Excel files, describe patterns in natural language, and automatically generate and apply regular expressions</p>
        </header>

        {error && (
          <div className="error">
            <strong>Error</strong> {error}
          </div>
        )}

        <div className="card">
          <h2>Step 1: Upload File</h2>
          <FileUpload
            onUploadSuccess={handleUploadSuccess}
            onUploadError={handleUploadError}
          />
        </div>

        {fileData && (
          <div className="card">
            <h2>Step 2: Data Preview</h2>
            <DataTable data={fileData} columns={columns} />
          </div>
        )}

        {fileData && (
          <div className="card">
            <h2>Step 3: Set Matching Pattern</h2>
            <PatternInput
              columns={columns}
              onProcess={handleProcess}
              isProcessing={isProcessing}
            />
          </div>
        )}

        {result && (
          <div className="card">
            <ResultDisplay
              result={result}
              onDownload={handleDownload}
            />
          </div>
        )}

        <footer className="app-footer">
          <p>Using Google Gemini API for natural language to regular expression conversion</p>
        </footer>
      </div>
    </div>
  )
}

export default App
