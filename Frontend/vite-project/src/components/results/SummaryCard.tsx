import React from 'react';

interface SummaryCardProps {
  summary: string;
}

const SummaryCard: React.FC<SummaryCardProps> = ({ summary }) => {
  // Clean up the summary text
  const cleanedSummary = summary.replace(/\\boxed{\n|"\n\nAlternatively.*$/g, '').replace(/^"|"$/g, '');

  return (
    <div className="bg-white rounded-2xl shadow-lg overflow-hidden transform transition-all duration-300 hover:shadow-xl">
      {/* Decorative top bar with gradient */}
      <div className="h-2 bg-gradient-to-r from-blue-500 to-indigo-600"></div>

      <div className="p-6 md:p-8">
        <div className="flex items-center mb-6">
          {/* Modern icon with gradient background */}
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full opacity-20 animate-pulse"></div>
            <div className="bg-gradient-to-r from-blue-500 to-indigo-500 p-3 rounded-full shadow-md relative">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
          </div>

          {/* Heading with subtitle */}
          <div className="ml-4">
            <h2 className="text-xl md:text-2xl font-heading font-bold text-gray-800">
              Analysis Summary
            </h2>
            <p className="text-sm text-gray-500">Key insights and findings</p>
          </div>
        </div>

        {/* Content area with improved typography */}
        <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
          <p className="whitespace-pre-line text-gray-700 leading-relaxed font-sans">
            {cleanedSummary}
          </p>
        </div>

        {/* Bottom area with decorative element */}
        <div className="flex justify-end mt-6">
          <div className="inline-flex items-center text-xs text-gray-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4 mr-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
            AI-powered analysis
          </div>
        </div>
      </div>
    </div>
  );
};

export default SummaryCard;
