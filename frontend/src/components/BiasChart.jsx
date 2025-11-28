import React from 'react'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

function BiasChart({ articles, frameSummary }) {
  // Prepare data from articles or frameSummary
  const sources = frameSummary || articles?.map(a => ({
    source: a.source,
    bias_index: a.bias_index || 0,
    transparency_score: 100 - (a.omission_score || 0) * 100,
  })) || []

  const data = {
    labels: sources.map(s => s.source),
    datasets: [
      {
        label: 'Bias Index',
        data: sources.map(s => s.bias_index || 0),
        backgroundColor: sources.map(s =>
          s.bias_index > 70 ? 'rgba(239, 68, 68, 0.6)' :
          s.bias_index > 40 ? 'rgba(234, 179, 8, 0.6)' :
          'rgba(34, 197, 94, 0.6)'
        ),
        borderColor: sources.map(s =>
          s.bias_index > 70 ? 'rgba(239, 68, 68, 1)' :
          s.bias_index > 40 ? 'rgba(234, 179, 8, 1)' :
          'rgba(34, 197, 94, 1)'
        ),
        borderWidth: 1,
      },
      {
        label: 'Transparency Score',
        data: sources.map(s => s.transparency_score || 0),
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Bias Index & Transparency by Source',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
      },
    },
  }

  if (sources.length === 0) {
    return (
      <p className="text-sm text-gray-500">No data available for chart.</p>
    )
  }

  return (
    <div style={{ height: '400px' }}>
      <Bar data={data} options={options} />
    </div>
  )
}

export default BiasChart

