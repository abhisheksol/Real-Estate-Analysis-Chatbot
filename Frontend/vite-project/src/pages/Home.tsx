import { useState } from 'react'
import axios from 'axios'
import QueryForm from '../components/QueryForm'
import ErrorMessage from '../components/ErrorMessage'
import ResultsSection from '../components/results/ResultsSection'
import LoadingIndicator from '../components/LoadingIndicator'

// Define the proper result interface
interface Dataset {
  label: string;
  data: number[];
}

interface Result {
  summary: string;
  chart: {
    labels: string[];
    data?: number[];
    datasets?: Dataset[];
  };
  table: Record<string, any>[];
}

function Home() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState<Result>({
    summary: '',
    chart: { labels: [] },
    table: []
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError('')
    
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/analyze/', { query })
      
      // Format data if needed
      let formattedResult = response.data;
      
      // Handle edge cases and ensure data is in expected format
      if (!formattedResult.chart) {
        formattedResult.chart = { labels: [] };
      }
      
      setResult(formattedResult)
    } catch (err) {
      setError('Error fetching data. Please try again.')
      console.error('API error:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-10">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
            Real Estate Analysis <span className="text-blue-600">Chatbot</span>
          </h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Get detailed analysis and insights about real estate properties and markets across locations
          </p>
        </div>
        
        <div className="bg-white rounded-2xl shadow-lg p-6 md:p-8 mb-8">
          <QueryForm 
            query={query} 
            setQuery={setQuery} 
            loading={loading} 
            handleSubmit={handleSubmit} 
          />
          
          {loading && <LoadingIndicator />}
          
          {error && <ErrorMessage message={error} />}
        </div>
        
        {result.summary && <ResultsSection result={result} />}
      </div>
    </div>
  )
}

export default Home
