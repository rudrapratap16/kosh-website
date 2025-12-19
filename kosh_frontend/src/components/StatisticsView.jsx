import React from 'react';

const StatisticsView = ({ statistics, darkMode, unit }) => {
  const formatValue = (value) => {
    if (value === null || value === undefined) return 'N/A';
    return `${value.toFixed(2)}${unit ? ` ${unit}` : ''}`;
  };

  return (
    <div>
      <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-gray-100' : 'text-gray-800'}`}>
        Statistical Summary
      </h2>
      <div className="grid grid-cols-4 gap-4">
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-blue-900/30' : 'bg-blue-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Count</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>
            {statistics.count || 'N/A'}
          </p>
        </div>
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-red-900/30' : 'bg-red-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Minimum</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-red-400' : 'text-red-600'}`}>
            {formatValue(statistics.min)}
          </p>
        </div>
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-green-900/30' : 'bg-green-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Average</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-green-400' : 'text-green-600'}`}>
            {formatValue(statistics.mean)}
          </p>
        </div>
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-purple-900/30' : 'bg-purple-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Median</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-purple-400' : 'text-purple-600'}`}>
            {formatValue(statistics.median)}
          </p>
        </div>
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Maximum</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`}>
            {formatValue(statistics.max)}
          </p>
        </div>
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-yellow-900/30' : 'bg-yellow-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Std Deviation</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-yellow-400' : 'text-yellow-600'}`}>
            {formatValue(statistics.std_dev)}
          </p>
        </div>
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-orange-900/30' : 'bg-orange-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Variance</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-orange-400' : 'text-orange-600'}`}>
            {formatValue(statistics.variance)}
          </p>
        </div>
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-pink-900/30' : 'bg-pink-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Kurtosis</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-pink-400' : 'text-pink-600'}`}>
            {statistics.kurtosis?.toFixed(2) || 'N/A'}
          </p>
        </div>
        <div className={`p-4 rounded-lg ${darkMode ? 'bg-teal-900/30' : 'bg-teal-50'}`}>
          <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Skewness</p>
          <p className={`text-2xl font-bold ${darkMode ? 'text-teal-400' : 'text-teal-600'}`}>
            {statistics.skewness?.toFixed(2) || 'N/A'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default StatisticsView;