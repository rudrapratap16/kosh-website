import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const FilterBar = ({ filters, options, onFilterChange, onDateChange, onApply, loading, onCollapseChange  }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div 
      className={`fixed left-0 top-0 h-full bg-white shadow-lg transition-all duration-300 z-10 group ${
        isCollapsed ? 'w-12' : 'w-80'
      }`}
    >
      {/* Toggle Button - Inside sidebar */}
      <button
  onClick={() => {
    setIsCollapsed(!isCollapsed);
    onCollapseChange?.(!isCollapsed); // Add this line
  }}
  className="absolute right-2 top-6 bg-gray-100 hover:bg-gray-200 rounded p-2 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
>
        {isCollapsed ? (
          <ChevronRight className="w-4 h-4 text-gray-600" />
        ) : (
          <ChevronLeft className="w-4 h-4 text-gray-600" />
        )}
      </button>

      {/* Sidebar Content */}
      <div className={`h-full overflow-y-auto p-6 pt-16 ${isCollapsed ? 'invisible' : 'visible'}`}>
        <h2 className="text-xl font-bold text-gray-800 mb-6">Filters</h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Outfall
            </label>
            <select
              value={filters.outfall}
              onChange={(e) => onFilterChange('outfall', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Outfall</option>
              {options.outfalls.map(outfall => (
                <option key={outfall} value={outfall}>{outfall}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Parameters
            </label>
            <select
              value={filters.parameter}
              onChange={(e) => onFilterChange('parameter', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Parameter</option>
              {options.parameters.map(param => (
                <option key={param} value={param}>{param}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Base
            </label>
            <select
              value={filters.base}
              onChange={(e) => onFilterChange('base', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Base</option>
              {options.bases.map(base => (
                <option key={base} value={base}>{base}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Unit
            </label>
            <select
              value={filters.unit}
              onChange={(e) => onFilterChange('unit', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select Unit</option>
              {options.units.map(unit => (
                <option key={unit} value={unit}>{unit}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Start Date
            </label>
            <input
              type="date"
              value={filters.startDate}
              onChange={(e) => onDateChange('startDate', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              End Date
            </label>
            <input
              type="date"
              value={filters.endDate}
              onChange={(e) => onDateChange('endDate', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <button
          onClick={onApply}
          disabled={loading}
          className="w-full mt-6 px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-400 transition-colors"
        >
          {loading ? 'Loading...' : 'Apply Filters'}
        </button>
      </div>
    </div>
  );
};

export default FilterBar;