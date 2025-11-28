import React from 'react'

function FactHeatmap({ facts, articles }) {
  if (!facts || facts.length === 0 || !articles || articles.length === 0) {
    return (
      <p className="text-sm text-gray-500">No data available for heatmap.</p>
    )
  }

  // Create a matrix: facts (rows) x articles (columns)
  const sources = [...new Set(articles.map(a => a.source))]
  
  // Check which facts are present in which articles
  const matrix = facts.map(fact => {
    const factText = fact.fact?.toLowerCase() || ''
    return sources.map(source => {
      const article = articles.find(a => a.source === source)
      if (!article) return false
      
      // Simple keyword matching (in production, use semantic similarity)
      const factKeywords = factText.split(' ').filter(w => w.length > 3)
      const articleText = article.text?.toLowerCase() || ''
      
      return factKeywords.some(keyword => articleText.includes(keyword))
    })
  })

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border-collapse">
        <thead>
          <tr>
            <th className="border p-2 text-left text-xs font-medium text-gray-700 bg-gray-50">
              Fact
            </th>
            {sources.map((source, idx) => (
              <th
                key={idx}
                className="border p-2 text-xs font-medium text-gray-700 bg-gray-50"
                title={source}
              >
                {source.substring(0, 15)}...
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {facts.map((fact, factIdx) => (
            <tr key={factIdx}>
              <td className="border p-2 text-xs text-gray-700 max-w-xs">
                <div className="truncate" title={fact.fact}>
                  {fact.fact?.substring(0, 50)}...
                </div>
              </td>
              {sources.map((source, sourceIdx) => {
                const isPresent = matrix[factIdx]?.[sourceIdx]
                return (
                  <td
                    key={sourceIdx}
                    className={`border p-2 text-center ${
                      isPresent
                        ? 'bg-green-200'
                        : 'bg-red-100'
                    }`}
                    title={isPresent ? 'Fact present' : 'Fact omitted'}
                  >
                    {isPresent ? '✓' : '✗'}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4 flex items-center space-x-4 text-xs text-gray-600">
        <div className="flex items-center">
          <div className="w-4 h-4 bg-green-200 mr-2"></div>
          <span>Fact Present</span>
        </div>
        <div className="flex items-center">
          <div className="w-4 h-4 bg-red-100 mr-2"></div>
          <span>Fact Omitted</span>
        </div>
      </div>
    </div>
  )
}

export default FactHeatmap

