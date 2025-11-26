import React from 'react';

const StatisticsView = ({ statistics, darkMode }) => {
  return (
    <div>
      <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-gray-100' : 'text-gray-800'}`}>
        Statistical Summary
      </h2>
      {statistics ? (
        <div className="grid grid-cols-4 gap-4">
          <div className={`p-4 rounded-lg ${darkMode ? 'bg-blue-900/30' : 'bg-blue-50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Count</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-blue-400' : 'text-blue-600'}`}>
              {statistics.count}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${darkMode ? 'bg-red-900/30' : 'bg-red-50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Minimum</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-red-400' : 'text-red-600'}`}>
              {statistics.min?.toFixed(2) || 'N/A'}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${darkMode ? 'bg-green-900/30' : 'bg-green-50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Average</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-green-400' : 'text-green-600'}`}>
              {statistics.mean?.toFixed(2) || 'N/A'}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${darkMode ? 'bg-purple-900/30' : 'bg-purple-50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Median</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-purple-400' : 'text-purple-600'}`}>
              {statistics.median?.toFixed(2) || 'N/A'}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${darkMode ? 'bg-indigo-900/30' : 'bg-indigo-50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Maximum</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-indigo-400' : 'text-indigo-600'}`}>
              {statistics.max?.toFixed(2) || 'N/A'}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${darkMode ? 'bg-yellow-900/30' : 'bg-yellow-50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Std Deviation</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-yellow-400' : 'text-yellow-600'}`}>
              {statistics.std_dev?.toFixed(2) || 'N/A'}
            </p>
          </div>
          <div className={`p-4 rounded-lg ${darkMode ? 'bg-orange-900/30' : 'bg-orange-50'}`}>
            <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-600'}`}>Variance</p>
            <p className={`text-2xl font-bold ${darkMode ? 'text-orange-400' : 'text-orange-600'}`}>
              {statistics.variance?.toFixed(2) || 'N/A'}
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
      ) : (
        <p className={`text-center py-8 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          No statistics available. Please select filters and click Apply.
        </p>
      )}
    </div>
  );
};

export default StatisticsView;