import React from 'react'

function FactSummary({ facts, summary }) {
  return (
    <div className="space-y-4">
      {summary && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
          <p className="text-sm text-blue-900 whitespace-pre-line">{summary}</p>
        </div>
      )}

      {facts && facts.length > 0 ? (
        <div className="space-y-3">
          <h4 className="font-medium text-gray-700">Verified Facts:</h4>
          {facts.map((fact, idx) => (
            <div
              key={idx}
              className={`border-l-4 pl-4 py-2 ${
                fact.status === 'supported' ? 'border-green-500 bg-green-50' :
                fact.status === 'contradicted' ? 'border-red-500 bg-red-50' :
                'border-yellow-500 bg-yellow-50'
              }`}
            >
              <p className="text-sm text-gray-800 mb-1">{fact.fact}</p>
              <div className="flex items-center justify-between text-xs text-gray-600">
                <span className={`px-2 py-1 rounded ${
                  fact.status === 'supported' ? 'bg-green-200 text-green-800' :
                  fact.status === 'contradicted' ? 'bg-red-200 text-red-800' :
                  'bg-yellow-200 text-yellow-800'
                }`}>
                  {fact.status}
                </span>
                <span>{fact.sources?.length || 0} sources</span>
              </div>
              {fact.quotes && fact.quotes.length > 0 && (
                <div className="mt-2 text-xs text-gray-600 italic">
                  "{fact.quotes[0].substring(0, 100)}..."
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <p className="text-sm text-gray-500">No facts extracted yet.</p>
      )}
    </div>
  )
}

export default FactSummary

