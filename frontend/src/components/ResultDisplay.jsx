/**
 * result display component
 * shows processed data and stats
 * including regex pattern and replacement info
 */
import React from 'react'
import DataTable from './DataTable'
import './ResultDisplay.css'


const ResultDisplay = ({ result, onDownload }) => {
  if (!result) {
    return null
  }

  try {
    const {
      processed_data,
      state,
      stats,
      regex_pattern,
      replacement,
      model_used,
    } = result

    const rawStats = stats || state || {}
    const normalizedStats = {
      total_rows: rawStats.total_rows ?? 0,
      matched_rows: rawStats.matched_rows ?? 0,
      replaced_count: rawStats.replaced_rows ?? rawStats.replaced_count ?? 0,
      unmatched_rows: rawStats.unmatched_rows ?? 0,
    }

    if (!processed_data || !Array.isArray(processed_data)) {
      return (
        <div className="result-display-container">
          <h3>Results</h3>
          <div className="error">
            <strong>Error:</strong> Invalid processed data format. Expected an array.
          </div>
        </div>
      )
    }

    return (
      <div className="result-display-container">
        <h3>Results</h3>

        <div className="result-stats">
          <div className="stat-item">
            <span className="stat-label">Total Rows:</span>
            <span className="stat-value">{normalizedStats.total_rows}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Matched Rows:</span>
            <span className="stat-value">{normalizedStats.matched_rows}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Replaced Count:</span>
            <span className="stat-value">{normalizedStats.replaced_count}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Unmatched Rows:</span>
            <span className="stat-value">{normalizedStats.unmatched_rows}</span>
          </div>
        </div>

        <div className="result-info">
          <div className="info-item">
            <strong>Generated Regex Pattern:</strong>
            <code className="regex-pattern">{regex_pattern}</code>
          </div>
          <div className="info-item">
            <strong>Replacement Value:</strong>
            <span>{replacement}</span>
          </div>
          {model_used && (
            <div className="info-item">
              <strong>Patten Used:</strong>
              <span>{model_used}</span>
            </div>
          )}
        </div>

        <div className="result-data">
          <h4>Processed Data</h4>
          <DataTable data={processed_data} />
        </div>

        {onDownload && (
          <div className="result-actions">
            <button onClick={() => onDownload(processed_data)} className="btn btn-primary">
              Download Processed Data
            </button>
          </div>
        )}
      </div>
    )
  } catch (error) {
    return (
      <div className="result-display-container">
        <h3>Results</h3>
        <div className="error">
          <strong>Error rendering results:</strong> {error?.message || String(error)}
        </div>
      </div>
    )
  }
}

export default ResultDisplay
