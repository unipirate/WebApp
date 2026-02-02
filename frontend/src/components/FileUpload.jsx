/**
 * File upload component
 * supports drag-and-drop and file selection
 * handles CSV, XLSX, XLS formats
 * displays upload status and errors
 */
import React, { useState } from 'react'
import { uploadFile } from '../services/api'
import './FileUpload.css'

const FileUpload = ({ onUploadSuccess, onUploadError }) => {

  const [isDragging, setIsDragging] = useState(false)
  
  const [isUploading, setIsUploading] = useState(false)
  
  const [error, setError] = useState(null)

  const handleFileSelect = async (event) => {
    const file = event.target.files[0]
        if (file) {
      await uploadFileHandler(file)
    }
  }

  const handleDragEnter = (event) => {
    event.preventDefault()
    event.stopPropagation()
    
    setIsDragging(true)
  }

  const handleDragLeave = (event) => {
    event.preventDefault()
    event.stopPropagation()
    
    setIsDragging(false)
  }

  const handleDragOver = (event) => {
    event.preventDefault()
    event.stopPropagation()
  }

  const handleDrop = async (event) => {
    event.preventDefault()
    event.stopPropagation()
    
    setIsDragging(false)

    const file = event.dataTransfer.files[0]
        if (file) {
      await uploadFileHandler(file)
    }
  }

  const uploadFileHandler = async (file) => {
    const allowedTypes = ['.csv', '.xlsx', '.xls']
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()
    
    if (!allowedTypes.includes(fileExtension)) {
      const errorMsg = `Unsupported file format. Supported formats: ${allowedTypes.join(', ')}`
      setError(errorMsg)
      
      if (onUploadError) {
        onUploadError(errorMsg)
      }
      return
    }

    const maxSize = 10 * 1024 * 1024
    if (file.size > maxSize) {
      const errorMsg = `File over the limited (${maxSize / 1024 / 1024}MB)`
      setError(errorMsg)
      
      if (onUploadError) {
        onUploadError(errorMsg)
      }
      return
    }

    setIsUploading(true)
    setError(null)

    try {
      const response = await uploadFile(file)
      
      if (onUploadSuccess) {
        onUploadSuccess(response)
      }
    } catch (err) {
      const errorMsg = err.response?.data?.message || err.message || 'File upload failed'
      setError(errorMsg)
      
      if (onUploadError) {
        onUploadError(errorMsg)
      }
    } finally {
      setIsUploading(false)
    }
  }


  return (
    <div className="file-upload-container">
      <div
        className={`file-upload-area ${isDragging ? 'dragging' : ''} ${isUploading ? 'uploading' : ''}`}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {isUploading ? (
          <div className="upload-status">
            <div className="spinner"></div>
            <p>UpLoading file...</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📁</div>
            <p className="upload-text">
              Drag and drop file here or <span className="upload-link">click to select file</span>
            </p>
            <p className="upload-hint">Supported formats: CSV, XLSX, XLS. Max size: 10MB</p>
            
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileSelect}
              className="file-input"
              disabled={isUploading}
            />
          </>
        )}
      </div>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
    </div>
  )
}

export default FileUpload
