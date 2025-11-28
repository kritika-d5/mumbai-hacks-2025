import React, { useState } from 'react'

function SearchForm({ onSubmit, disabled }) {
  const [query, setQuery] = useState('')
  const [dateFrom, setDateFrom] = useState('')
  const [dateTo, setDateTo] = useState('')
  const [sources, setSources] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const formData = {
      query,
      dateFrom: dateFrom || null,
      dateTo: dateTo || null,
      sources: sources ? sources.split(',').map(s => s.trim()) : null,
    }

    onSubmit(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-1">
          Search Query
        </label>
        <input
          type="text"
          id="query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          required
          disabled={disabled}
          placeholder="e.g., climate change, election results"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="dateFrom" className="block text-sm font-medium text-gray-700 mb-1">
            From Date (optional)
          </label>
          <input
            type="date"
            id="dateFrom"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            disabled={disabled}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
          />
        </div>

        <div>
          <label htmlFor="dateTo" className="block text-sm font-medium text-gray-700 mb-1">
            To Date (optional)
          </label>
          <input
            type="date"
            id="dateTo"
            value={dateTo}
            onChange={(e) => setDateTo(e.target.value)}
            disabled={disabled}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
          />
        </div>
      </div>

      <div>
        <label htmlFor="sources" className="block text-sm font-medium text-gray-700 mb-1">
          Sources (optional, comma-separated)
        </label>
        <input
          type="text"
          id="sources"
          value={sources}
          onChange={(e) => setSources(e.target.value)}
          disabled={disabled}
          placeholder="e.g., bbc-news, cnn, reuters"
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100"
        />
      </div>

      <button
        type="submit"
        disabled={disabled || !query}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {disabled ? 'Analyzing...' : 'Analyze News'}
      </button>
    </form>
  )
}

export default SearchForm

