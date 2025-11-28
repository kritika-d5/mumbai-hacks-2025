import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import SearchPage from './pages/SearchPage'
import ClusterDetailPage from './pages/ClusterDetailPage'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <h1 className="text-2xl font-bold text-gray-900">NewsPrism</h1>
            <p className="text-sm text-gray-600">News Bias Analysis Platform</p>
          </div>
        </header>
        
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/cluster/:clusterId" element={<ClusterDetailPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

