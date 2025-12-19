import React, { useState, useEffect } from 'react';
import { Sun, Moon } from 'lucide-react';
import FilterBar from './components/FilterBar';
import TabBar from './components/TabBar';
import GraphView from './components/GraphView';
import RawDataView from './components/RawDataView';
import StatisticsView from './components/StatisticsView';
import { 
  fetchInitialFilters, 
  fetchCascadingFilters, 
  fetchCombinedData,
  fetchCombinedStatistics
} from './apis.js';

const App = () => {
  const [darkMode, setDarkMode] = useState(false);

  // Helper function to format date as YYYY-MM-DD
  const formatDate = (date) => {
    return date.toISOString().split('T')[0];
  };

  // Calculate default dates
  const getDefaultDates = () => {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setFullYear(startDate.getFullYear() - 1);
    
    return {
      startDate: formatDate(startDate),
      endDate: formatDate(endDate)
    };
  };

  const defaultDates = getDefaultDates();

  const [filters, setFilters] = useState({
    permit_number: '',
    outfall: '',
    parameter: '',
    base: '',
    unit: '',
    startDate: defaultDates.startDate,
    endDate: defaultDates.endDate
  });

  const [options, setOptions] = useState({
    permit_numbers: [],
    outfalls: [],
    parameters: [],
    bases: [],
    units: []
  });

  
  const [activeTab, setActiveTab] = useState('graph');
  const [data, setData] = useState([]);
  const [allFacilityData, setAllFacilityData] = useState([]); // NEW: Store all facility data
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  useEffect(() => {
    loadInitialFilters();
  }, []);

  useEffect(() => {
    const allFiltersSelected = filters.parameter && 
                               filters.base && 
                               filters.unit &&
                               filters.startDate &&
                               filters.endDate;
    
    if (allFiltersSelected) {
      handleApplyFilters();
    }
  }, [filters]);

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
    let newFilters = { ...filters };
    
    newFilters[filterName] = value;
    
    // Clear dependent filters based on hierarchy
    if (filterName === 'permit_number') {
      newFilters.outfall = '';
      newFilters.parameter = '';
      newFilters.base = '';
      newFilters.unit = '';
    } else if (filterName === 'outfall') {
      newFilters.parameter = '';
      newFilters.base = '';
      newFilters.unit = '';
    } else if (filterName === 'parameter') {
      newFilters.base = '';
      newFilters.unit = '';
    } else if (filterName === 'base') {
      newFilters.unit = '';
    }
    
    setFilters(newFilters);

    try {
      const cascadingData = await fetchCascadingFilters({
        permit_number: newFilters.permit_number || null,
        outfall: newFilters.outfall || null,
        parameter: newFilters.parameter || null,
        base: newFilters.base || null
      });
      console.log('Cascading filter data:', cascadingData);
      setOptions(cascadingData);
    } catch (error) {
      console.error('Error fetching cascading filters:', error);
    }
  };

  const handleApplyFilters = async () => {
    setLoading(true);
    try {
      // Fetch filtered data for graph and statistics
      const [dataResult, statsResult] = await Promise.all([
        fetchCombinedData(filters),
        fetchCombinedStatistics(filters)
      ]);
      
      setData(dataResult.data || []);
      setStatistics(statsResult);
      
      // NEW: Fetch all facility data (only permit_number, outfall, and date range)
      const facilityFilters = {
        permit_number: filters.permit_number,
        outfall: filters.outfall,
        startDate: filters.startDate,
        endDate: filters.endDate
        // Intentionally exclude parameter, base, and unit
      };
      
      const allDataResult = await fetchCombinedData(facilityFilters);
      setAllFacilityData(allDataResult.data || []);
      
    } catch (error) {
      console.error('Error fetching data:', error);
      setData([]);
      setAllFacilityData([]);
      setStatistics(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900' : 'bg-gray-50'}`}>
      <FilterBar
        filters={filters}
        options={options}
        onFilterChange={handleFilterChange}
        onDateChange={(field, value) => setFilters({ ...filters, [field]: value })}
        onApply={handleApplyFilters}
        loading={loading}
        onCollapseChange={setSidebarCollapsed}
        darkMode={darkMode}
      />

      {/* Main content area with dynamic left margin */}
      <div 
        className="transition-all duration-300 p-6" 
        style={{ marginLeft: sidebarCollapsed ? '48px' : '320px' }}
      >
        {/* Dark Mode Toggle Button */}
        <button
          onClick={() => setDarkMode(!darkMode)}
          className={`fixed top-6 right-6 p-3 rounded-full shadow-lg transition-colors duration-300 z-20 focus:outline-none focus:ring-0 active:outline-none ${
            darkMode 
              ? 'bg-gray-800 hover:bg-gray-700 text-yellow-400' 
              : 'bg-white hover:bg-gray-100 text-gray-700'
          }`}
          style={{ 
            outline: 'none',
            boxShadow: darkMode ? '0 10px 15px -3px rgba(0, 0, 0, 0.3)' : '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
            WebkitTapHighlightColor: 'transparent'
          }}
          onFocus={(e) => e.target.blur()}
          title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </button>

        <div className="max-w-7xl mx-auto">
          <TabBar activeTab={activeTab} setActiveTab={setActiveTab} darkMode={darkMode} />

          <div className={`rounded-lg shadow p-6 transition-colors duration-300 ${
            darkMode ? 'bg-gray-800' : 'bg-white'
          }`}>
            {activeTab === 'graph' && (
              <div>
                <GraphView data={data} filters={filters} darkMode={darkMode} />
                {statistics && (
                  <div className="mt-8">
                    <StatisticsView statistics={statistics} darkMode={darkMode} unit={filters.unit}/>
                  </div>
                )}
              </div>
            )}
            {activeTab === 'rawdata' && (
              <RawDataView 
                data={allFacilityData} 
                darkMode={darkMode} 
                filters={filters}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;