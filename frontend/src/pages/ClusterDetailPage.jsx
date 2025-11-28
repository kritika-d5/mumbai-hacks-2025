import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { getCluster } from '../services/api'
import LoadingSpinner from '../components/LoadingSpinner'
import FactSummary from '../components/FactSummary'
import FrameAnalysis from '../components/FrameAnalysis'
import BiasChart from '../components/BiasChart'
import FactHeatmap from '../components/FactHeatmap'

function ClusterDetailPage() {
  const { clusterId } = useParams()
  const [cluster, setCluster] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchCluster = async () => {
      try {
        const data = await getCluster(clusterId)
        setCluster(data)
      } catch (err) {
        setError(err.response?.data?.detail || err.message || 'Failed to load cluster')
      } finally {
        setLoading(false)
      }
    }

    fetchCluster()
  }, [clusterId])

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    )
  }

  if (!cluster) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center text-gray-500">
        Cluster not found
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-2xl font-bold mb-2">Cluster Analysis</h2>
        <p className="text-gray-600">Query: {cluster.query}</p>
        <p className="text-sm text-gray-500 mt-2">
          {cluster.articles?.length || 0} articles • Created {new Date(cluster.created_at).toLocaleDateString()}
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Fact Summary</h3>
          <FactSummary facts={cluster.facts} summary={cluster.fact_summary} />
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Framing Analysis</h3>
          <FrameAnalysis frameSummary={cluster.frame_summary} articles={cluster.articles} />
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">Bias Index Comparison</h3>
        <BiasChart articles={cluster.articles} frameSummary={cluster.frame_summary} />
      </div>

      {cluster.facts && cluster.facts.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Fact Coverage Heatmap</h3>
          <FactHeatmap facts={cluster.facts} articles={cluster.articles} />
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold mb-4">Articles</h3>
        <div className="space-y-4">
          {cluster.articles?.map((article) => (
            <ArticleCard key={article.id} article={article} />
          ))}
        </div>
      </div>
    </div>
  )
}

function ArticleCard({ article }) {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h4 className="font-semibold text-lg">{article.title}</h4>
        <div className="flex items-center space-x-2">
          {article.bias_index !== null && (
            <span className={`px-2 py-1 rounded text-xs font-medium ${
              article.bias_index > 70 ? 'bg-red-100 text-red-800' :
              article.bias_index > 40 ? 'bg-yellow-100 text-yellow-800' :
              'bg-green-100 text-green-800'
            }`}>
              Bias: {article.bias_index.toFixed(1)}
            </span>
          )}
        </div>
      </div>
      <p className="text-sm text-gray-600 mb-2">
        {article.source} • {new Date(article.published_at).toLocaleDateString()}
      </p>
      <p className="text-sm text-gray-700 line-clamp-2">{article.text.substring(0, 200)}...</p>
      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:underline text-sm mt-2 inline-block"
      >
        Read full article →
      </a>
    </div>
  )
}

export default ClusterDetailPage

