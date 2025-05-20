import React from 'react';
import SummaryCard from './SummaryCard';
import ChartCard from './ChartCard';
import DataTable from './DataTable';

interface Dataset {
  label: string;
  data: number[];
}

interface ResultsProps {
  result: {
    summary: string;
    chart: {
      labels: string[];
      data?: number[];
      datasets?: Dataset[];
    };
    table: Record<string, any>[];
  };
}

const ResultsSection: React.FC<ResultsProps> = ({ result }) => {
  const hasChartData = result.chart && 
    result.chart.labels && 
    result.chart.labels.length > 0 && 
    (result.chart.data || result.chart.datasets);

  return (
    <div className="space-y-6 md:space-y-8 animate-fadeIn">
      <SummaryCard summary={result.summary} />
      
      {hasChartData && (
        <ChartCard 
          labels={result.chart.labels} 
          data={result.chart.data} 
          datasets={result.chart.datasets}
        />
      )}

      {result.table && result.table.length > 0 && (
        <DataTable data={result.table} />
      )}
    </div>
  );
};

export default ResultsSection;
