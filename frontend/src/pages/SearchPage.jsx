import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyzeQuery } from '../services/api'
import SearchForm from '../components/SearchForm'
import LoadingSpinner from '../components/LoadingSpinner'
import ClusterCard from '../components/ClusterCard'

function SearchPage() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const handleSearch = async (formData) => {
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const data = await analyzeQuery(
        formData.query,
        formData.dateFrom,
        formData.dateTo,
        formData.sources
      )
      setResults(data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleClusterClick = (clusterId) => {
    navigate(`/cluster/${clusterId}`)
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Search & Analyze News</h2>
        <SearchForm onSubmit={handleSearch} disabled={loading} />
      </div>

      {loading && (
        <div className="flex justify-center py-12">
          <LoadingSpinner />
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {results && (
        <div className="space-y-4">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">
              Analysis Results
            </h3>
            <p className="text-sm text-gray-600">
              Found {results.total_articles} articles across {results.clusters?.length || 0} clusters
            </p>
          </div>

          {results.clusters && results.clusters.length > 0 ? (
            <div className="grid gap-4">
              {results.clusters.map((cluster) => (
                <ClusterCard
                  key={cluster.cluster_id}
                  cluster={cluster}
                  onClick={() => handleClusterClick(cluster.cluster_id)}
                />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow p-6 text-center text-gray-500">
              No clusters found. Try a different query.
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default SearchPage

