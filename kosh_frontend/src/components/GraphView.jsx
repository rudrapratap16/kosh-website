import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const GraphView = ({ data }) => {
  const chartData = data.map(item => ({
    date: item.monitoring_period_date,
    value: parseFloat(item.dmr_value) || 0,
    limit: parseFloat(item.limit_value) || null
  }));

  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">DMR Values Over Time</h2>
      {console.log('GraphView data:', chartData)}
      {chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#3b82f6" name="DMR Value" />
            {chartData.some(d => d.limit !== null) && (
              <Line type="monotone" dataKey="limit" stroke="#ef4444" name="Limit Value" strokeDasharray="5 5" />
            )}
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <p className="text-gray-500 text-center py-8">No data available. Please select filters and click Apply.</p>
      )}
    </div>
  );
};

export default GraphView;