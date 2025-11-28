import React from 'react'

function FrameAnalysis({ frameSummary, articles }) {
  if (!frameSummary || frameSummary.length === 0) {
    return (
      <p className="text-sm text-gray-500">No framing analysis available.</p>
    )
  }

  return (
    <div className="space-y-4">
      {frameSummary.map((frame, idx) => (
        <div key={idx} className="border rounded-lg p-4">
          <div className="flex justify-between items-start mb-3">
            <h4 className="font-semibold">{frame.source}</h4>
            <div className="flex items-center space-x-2">
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                frame.bias_index > 70 ? 'bg-red-100 text-red-800' :
                frame.bias_index > 40 ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                Bias: {frame.bias_index?.toFixed(1) || 'N/A'}
              </span>
              <span className="px-2 py-1 rounded text-xs font-medium bg-blue-100 text-blue-800">
                Transparency: {frame.transparency_score?.toFixed(1) || 'N/A'}
              </span>
            </div>
          </div>

          <div className="mb-3">
            <div className="flex items-center space-x-2 mb-1">
              <span className="text-xs text-gray-600">Tone:</span>
              <div className="flex-1 bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full ${
                    frame.tone > 0.3 ? 'bg-green-500' :
                    frame.tone < -0.3 ? 'bg-red-500' :
                    'bg-yellow-500'
                  }`}
                  style={{
                    width: `${Math.abs(frame.tone) * 100}%`,
                    marginLeft: frame.tone < 0 ? 'auto' : '0'
                  }}
                />
              </div>
              <span className="text-xs text-gray-600">
                {frame.tone > 0 ? '+' : ''}{frame.tone?.toFixed(2) || '0.00'}
              </span>
            </div>
          </div>

          {frame.top_phrases && frame.top_phrases.length > 0 && (
            <div>
              <p className="text-xs font-medium text-gray-700 mb-2">Loaded Phrases:</p>
              <div className="flex flex-wrap gap-2">
                {frame.top_phrases.slice(0, 5).map((phrase, pIdx) => (
                  <span
                    key={pIdx}
                    className="px-2 py-1 bg-orange-100 text-orange-800 rounded text-xs"
                    title={phrase.reason || phrase.type}
                  >
                    {phrase.phrase?.substring(0, 30)}...
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

export default FrameAnalysis

