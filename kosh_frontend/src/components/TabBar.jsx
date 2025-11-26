import React from 'react';

const TabBar = ({ activeTab, setActiveTab, darkMode }) => {
  return (
    <div className={`rounded-lg shadow mb-6 transition-colors duration-300 ${
      darkMode ? 'bg-gray-800' : 'bg-white'
    }`}>
      <div className={`flex ${darkMode ? 'border-b border-gray-700' : 'border-b border-gray-200'}`}>
        <button
          onClick={() => setActiveTab('graph')}
          className={`px-6 py-3 font-medium transition-colors focus:outline-none ${
            activeTab === 'graph'
              ? 'text-blue-500 border-b-2 border-blue-500'
              : darkMode 
                ? 'text-gray-400 hover:text-gray-200' 
                : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Graph
        </button>
        <button
          onClick={() => setActiveTab('statistics')}
          className={`px-6 py-3 font-medium transition-colors focus:outline-none ${
            activeTab === 'statistics'
              ? 'text-blue-500 border-b-2 border-blue-500'
              : darkMode 
                ? 'text-gray-400 hover:text-gray-200' 
                : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Statistics
        </button>
        <button
          onClick={() => setActiveTab('rawdata')}
          className={`px-6 py-3 font-medium transition-colors focus:outline-none ${
            activeTab === 'rawdata'
              ? 'text-blue-500 border-b-2 border-blue-500'
              : darkMode 
                ? 'text-gray-400 hover:text-gray-200' 
                : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Raw Data
        </button>
      </div>
    </div>
  );
};

export default TabBar;