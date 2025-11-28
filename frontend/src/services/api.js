import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const searchArticles = async (query, dateFrom, dateTo, sources, limit = 50) => {
  const response = await api.post('/search', {
    query,
    date_from: dateFrom,
    date_to: dateTo,
    sources,
    limit,
  })
  return response.data
}

export const analyzeQuery = async (query, dateFrom, dateTo, sources) => {
  const response = await api.post('/search/analyze', {
    query,
    date_from: dateFrom,
    date_to: dateTo,
    sources,
  })
  return response.data
}

export const getCluster = async (clusterId) => {
  const response = await api.get(`/search/clusters/${clusterId}`)
  return response.data
}

export const getArticle = async (articleId) => {
  const response = await api.get(`/search/articles/${articleId}`)
  return response.data
}

export default api

