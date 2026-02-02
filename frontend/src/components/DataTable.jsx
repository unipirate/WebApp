/**
 * data table component
 * displays data in a tabular format
 * use react-table for table functionalities
 */
import React, { useMemo } from 'react'
import { useTable } from 'react-table'
import './DataTable.css'

const DataTable = ({ data, columns }) => {
  const tableColumns = useMemo(() => {

    if (columns && columns.length > 0) {
      return columns.map(col => ({
        Header: col,
        accessor: col,
      }))
    } 

    else if (data && data.length > 0) {
      return Object.keys(data[0]).map(key => ({
        Header: key,
        accessor: key,
      }))
    }

    return []
  }, [data, columns])

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({
    columns: tableColumns,
    data: data || [],
  })

  if (!data || data.length === 0) {
    return (
      <div className="data-table-empty">
        <p>No data available. Please upload a file first.</p>
      </div>
    )
  }

  return (
    <div className="data-table-container">
      <div className="table-wrapper">
        <table {...getTableProps()} className="data-table">
          <thead>
            {headerGroups.map(headerGroup => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map(column => (
                  <th {...column.getHeaderProps()}>
                    {column.render('Header')}
                  </th>
                ))}
              </tr>
            ))}
          </thead>

          <tbody {...getTableBodyProps()}>
            {rows.map(row => {
              prepareRow(row)
              return (
                <tr {...row.getRowProps()}>
                  {row.cells.map(cell => (
                    <td {...cell.getCellProps()}>
                      {cell.render('Cell')}
                    </td>
                  ))}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <div className="table-info">
        <p>Total row number: {data.length}</p>
      </div>
    </div>
  )
}

export default DataTable
