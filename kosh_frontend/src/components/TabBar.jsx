import React from 'react';

const TabBar = ({ activeTab, setActiveTab }) => {
  return (
    <div className="bg-white rounded-lg shadow mb-6">
      <div className="flex border-b">
        <button
          onClick={() => setActiveTab('graph')}
          className={`px-6 py-3 font-medium ${
            activeTab === 'graph'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Graph
        </button>
        <button
          onClick={() => setActiveTab('statistics')}
          className={`px-6 py-3 font-medium ${
            activeTab === 'statistics'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-800'
          }`}
        >
          Statistics
        </button>
        <button
          onClick={() => setActiveTab('rawdata')}
          className={`px-6 py-3 font-medium ${
            activeTab === 'rawdata'
              ? 'text-blue-600 border-b-2 border-blue-600'
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