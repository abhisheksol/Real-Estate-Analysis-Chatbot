import React from 'react';

interface QueryFormProps {
  query: string;
  setQuery: (query: string) => void;
  loading: boolean;
  handleSubmit: (e: React.FormEvent) => void;
}

const QueryForm: React.FC<QueryFormProps> = ({ query, setQuery, loading, handleSubmit }) => {
  return (
    <form onSubmit={handleSubmit} className="relative">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Ask about properties</h2>
      <div className="flex flex-col md:flex-row gap-3">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="E.g., Compare Wakad and Akurdi demand trends"
          className="flex-1 px-4 py-3 rounded-lg border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-700"
          disabled={loading}
        />
        <button 
          type="submit" 
          className={`group relative px-6 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-center min-w-[130px] ${
            loading 
              ? 'cursor-not-allowed' 
              : 'hover:translate-y-[-1px] hover:shadow-lg active:translate-y-[1px]'
          }`}
          disabled={loading}
          style={{
            background: loading 
              ? 'linear-gradient(45deg, #93c5fd, #bfdbfe)'
              : 'linear-gradient(45deg, #2563eb, #3b82f6)',
            boxShadow: loading 
              ? '0 2px 6px rgba(147, 197, 253, 0.5)'
              : '0 4px 6px rgba(37, 99, 235, 0.25), 0 1px 3px rgba(37, 99, 235, 0.1)'
          }}
        >
          {loading ? (
            <div className="flex items-center justify-center text-white">
              <svg className="animate-spin mr-2 h-5 w-5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Processing...</span>
            </div>
          ) : (
            <>
              <span className="text-white relative z-10">Analyze</span>
              <svg 
                className="w-5 h-5 ml-2 text-white opacity-70 group-hover:translate-x-1 transition-transform duration-200" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24" 
                xmlns="http://www.w3.org/2000/svg"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
              </svg>
              <div className="absolute inset-0 rounded-lg bg-white opacity-0 group-hover:opacity-20 transition-opacity duration-200"></div>
            </>
          )}
        </button>
      </div>
      {!loading && (
        <p className="mt-2 text-sm text-gray-500">Try asking questions about property trends, comparisons, or specific areas like <b>Wakad ,Ambegaon Budruk , Akurdi , Aundh.</b></p>
      )}
    </form>
  );
};

export default QueryForm;
