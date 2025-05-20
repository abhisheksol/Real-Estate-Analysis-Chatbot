import React from 'react';

const LoadingIndicator: React.FC = () => {
  return (
    <div className="mt-6 bg-blue-50 rounded-lg p-4 flex items-center">
      <div className="relative mr-3">
        <div className="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
      </div>
      <div>
        <p className="font-medium text-blue-800">Processing your request</p>
        <p className="text-sm text-blue-600">Using Deepseek R1 model. This may take 10-20 seconds...</p>
      </div>
    </div>
  );
};

export default LoadingIndicator;
