/**
 * mode input component
 * allows users to input natural language patterns for matching and replacing
 * utilizes available column names for better context
 * handles form submission and validation
 */
import React, { useState } from 'react'
import './PatternInput.css'

const PatternInput = ({ columns, onProcess, isProcessing }) => {
  const [naturalLanguageInput, setNaturalLanguageInput] = useState('')
  const [error, setError] = useState(null)

  const handleSubmit = (event) => {
    event.preventDefault()
    setError(null)

    if (!naturalLanguageInput.trim()) {
      setError('Please enter a natural language description of the pattern to match and replace.')
      return
    }

    if (onProcess) {
      onProcess({
        natural_language_input: naturalLanguageInput.trim(),
      })
    }
  }


  const handleReset = () => {
    setNaturalLanguageInput('')
    setError(null)
  }


  const columnsHint = columns && columns.length > 0 
    ? `Available columns: ${columns.join(', ')}` 
    : ''

  return (
    <div className="pattern-input-container">
      <h3>Pattern Matching and Replacement</h3>
      
      <form onSubmit={handleSubmit} className="pattern-form">
        <div className="form-group">
          <label htmlFor="natural-language-input">Natural Language Description:</label>
          <textarea
            id="natural-language-input"
            value={naturalLanguageInput}
            onChange={(e) => setNaturalLanguageInput(e.target.value)}
            placeholder='e.g., "Replace all email addresses in the email column with \"REDACTED\"" or "Replace phone numbers in the phone column with \"***\""'
            className="form-input"
            disabled={isProcessing}
            rows={3}
            style={{ resize: 'vertical' }}
          />
          <small className="form-hint">
            Use complete natural language to describe the operation to be performed. The system will automatically identify column names, matching patterns, and replacement values.
            <br />
            Examples:
            <ul style={{ marginTop: '8px', marginBottom: '0', paddingLeft: '20px' }}>
              <li>Replace all email addresses in the email column with "REDACTED"</li>
              <li>Replace phone numbers in the phone column with "***"</li>
              <li>change "email" to "one page at a time"</li>
            </ul>
            {columnsHint && (
              <span style={{ display: 'block', marginTop: '8px', fontWeight: 'bold' }}>
                {columnsHint}
              </span>
            )}
          </small>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={isProcessing || !columns || columns.length === 0}
          >
            {isProcessing ? 'Processing...' : 'Start Processing'}
          </button>
          <button
            type="button"
            onClick={handleReset}
            className="btn btn-secondary"
            disabled={isProcessing}
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  )
}

export default PatternInput
