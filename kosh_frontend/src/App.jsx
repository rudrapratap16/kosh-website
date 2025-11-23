import React, { useState, useEffect } from 'react';
import FilterBar from './components/FilterBar';
import TabBar from './components/TabBar';
import GraphView from './components/GraphView';
import RawDataView from './components/RawDataView';
import StatisticsView from './components/StatisticsView';
import { fetchInitialFilters, fetchCascadingFilters, fetchData, fetchStatistics } from './apis.js';

const App = () => {
  const [filters, setFilters] = useState({
    outfall: '',
    parameter: '',
    base: '',
    unit: '',
    startDate: '',
    endDate: ''
  });

  const [options, setOptions] = useState({
    outfalls: [],
    parameters: [],
    bases: [],
    units: []
  });

  
  const [activeTab, setActiveTab] = useState('graph');
  const [data, setData] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  useEffect(() => {
    loadInitialFilters();
  }, []);

  const loadInitialFilters = async () => {
    try {
      const data = await fetchInitialFilters();
      console.log('Initial filter data:', data);
      setOptions(data);
    } catch (error) {
      console.error('Error fetching initial filters:', error);
    }
  };

  const handleFilterChange = async (filterName, value) => {
    const newFilters = { ...filters, [filterName]: value };
    setFilters(newFilters);

    try {
      const data = await fetchCascadingFilters({
        outfall: newFilters.outfall || null,
        parameter: newFilters.parameter || null,
        base: newFilters.base || null,
        unit: newFilters.unit || null
      });
      setOptions(data);
    } catch (error) {
      console.error('Error fetching cascading filters:', error);
    }
  };

  const handleApplyFilters = async () => {
    setLoading(true);
    try {
      const result = await fetchData(filters);
      setData(result.data || []);

      if (activeTab === 'statistics') {
        const statsResult = await fetchStatistics(filters);
        setStatistics(statsResult);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'statistics' && filters.outfall) {
      handleApplyFilters();
    }
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-gray-50">
      <FilterBar
        filters={filters}
        options={options}
        onFilterChange={handleFilterChange}
        onDateChange={(field, value) => setFilters({ ...filters, [field]: value })}
        onApply={handleApplyFilters}
        loading={loading}
        onCollapseChange={setSidebarCollapsed} // Add this line
      />

      {/* Main content area with dynamic left margin */}
      <div 
        className="transition-all duration-300 p-6" 
        style={{ marginLeft: sidebarCollapsed ? '48px' : '320px' }}
      >
        <div className="max-w-7xl mx-auto">
          <TabBar activeTab={activeTab} setActiveTab={setActiveTab} />

          <div className="bg-white rounded-lg shadow p-6">
            {activeTab === 'graph' && <GraphView data={data} />}
            {activeTab === 'statistics' && <StatisticsView statistics={statistics} />}
            {activeTab === 'rawdata' && <RawDataView data={data} />}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;