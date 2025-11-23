import React from 'react';

const StatisticsView = ({ statistics }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Statistical Summary</h2>
      {statistics ? (
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Count</p>
            <p className="text-2xl font-bold text-blue-600">{statistics.count}</p>
          </div>
          <div className="bg-red-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Minimum</p>
            <p className="text-2xl font-bold text-red-600">{statistics.min?.toFixed(2) || 'N/A'}</p>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Average</p>
            <p className="text-2xl font-bold text-green-600">{statistics.mean?.toFixed(2) || 'N/A'}</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Median</p>
            <p className="text-2xl font-bold text-purple-600">{statistics.median?.toFixed(2) || 'N/A'}</p>
          </div>
          <div className="bg-indigo-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Maximum</p>
            <p className="text-2xl font-bold text-indigo-600">{statistics.max?.toFixed(2) || 'N/A'}</p>
          </div>
          <div className="bg-yellow-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Std Deviation</p>
            <p className="text-2xl font-bold text-yellow-600">{statistics.std_dev?.toFixed(2) || 'N/A'}</p>
          </div>
          <div className="bg-orange-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Variance</p>
            <p className="text-2xl font-bold text-orange-600">{statistics.variance?.toFixed(2) || 'N/A'}</p>
          </div>
          <div className="bg-pink-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Kurtosis</p>
            <p className="text-2xl font-bold text-pink-600">{statistics.kurtosis?.toFixed(2) || 'N/A'}</p>
          </div>
          <div className="bg-teal-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600">Skewness</p>
            <p className="text-2xl font-bold text-teal-600">{statistics.skewness?.toFixed(2) || 'N/A'}</p>
          </div>
        </div>
      ) : (
        <p className="text-gray-500 text-center py-8">No statistics available. Please select filters and click Apply.</p>
      )}
    </div>
  );
};

export default StatisticsView;