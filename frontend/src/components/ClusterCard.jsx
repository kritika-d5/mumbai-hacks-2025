import React from 'react'

function ClusterCard({ cluster, onClick }) {
  const avgBias = cluster.bias_results?.length > 0
    ? cluster.bias_results.reduce((sum, r) => sum + (r.bias_index || 0), 0) / cluster.bias_results.length
    : 0

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-lg transition-shadow"
    >
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-lg font-semibold mb-1">Cluster</h3>
          <p className="text-sm text-gray-600">
            {cluster.articles_count} articles • {cluster.facts_count} facts
          </p>
        </div>
        <div className="text-right">
          <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
            avgBias > 70 ? 'bg-red-100 text-red-800' :
            avgBias > 40 ? 'bg-yellow-100 text-yellow-800' :
            'bg-green-100 text-green-800'
          }`}>
            Avg Bias: {avgBias.toFixed(1)}
          </div>
        </div>
      </div>

      {cluster.bias_results && cluster.bias_results.length > 0 && (
        <div className="space-y-2">
          <p className="text-sm font-medium text-gray-700">Sources:</p>
          <div className="flex flex-wrap gap-2">
            {cluster.bias_results.slice(0, 5).map((result, idx) => (
              <span
                key={idx}
                className="px-2 py-1 bg-gray-100 rounded text-xs"
              >
                {result.source}
              </span>
            ))}
            {cluster.bias_results.length > 5 && (
              <span className="px-2 py-1 bg-gray-100 rounded text-xs">
                +{cluster.bias_results.length - 5} more
              </span>
            )}
          </div>
        </div>
      )}

      <div className="mt-4 text-sm text-blue-600 hover:text-blue-800">
        View details →
      </div>
    </div>
  )
}

export default ClusterCard

