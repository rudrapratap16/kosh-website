import React, { useState, useEffect } from 'react';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { Sun, Moon } from 'lucide-react';
import LoginPage from './components/LoginPage';
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

const GOOGLE_CLIENT_ID = '569071530463-tmc25vftuc18maava7vdg1f6v56nk61t.apps.googleusercontent.com'; // Replace with your actual Google Client ID
const BACKEND_URL = 'https://kosh-backend-569071530463.europe-west1.run.app';
// const BACKEND_URL = 'http://localhost:8080';

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
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
  const [allFacilityData, setAllFacilityData] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  // Check if user is already logged in on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('jwt_token');
      const userInfo = localStorage.getItem('user_info');
      
      if (token && userInfo) {
        try {
          // Verify token with backend
          const response = await fetch(`${BACKEND_URL}/api/auth/verify`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          
          if (response.ok) {
            setUser(JSON.parse(userInfo));
            setIsAuthenticated(true);
          } else {
            // Token invalid, clear storage
            localStorage.removeItem('jwt_token');
            localStorage.removeItem('user_info');
          }
        } catch (error) {
          console.error('Auth check failed:', error);
          localStorage.removeItem('jwt_token');
          localStorage.removeItem('user_info');
        }
      }
      
      setAuthLoading(false);
    };

    checkAuth();
  }, []);

  useEffect(() => {
    if (isAuthenticated) {
      loadInitialFilters();
    }
  }, [isAuthenticated]);

  useEffect(() => {
    if (!isAuthenticated) return;
    
    const allFiltersSelected = filters.parameter && 
                               filters.base && 
                               filters.unit &&
                               filters.startDate &&
                               filters.endDate;
    
    if (allFiltersSelected) {
      handleApplyFilters();
    }
  }, [filters, isAuthenticated]);

  const handleLogin = (userInfo) => {
    setUser(userInfo);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('jwt_token');
    localStorage.removeItem('user_info');
    setUser(null);
    setIsAuthenticated(false);
  };

  const loadInitialFilters = async () => {
    try {
      const data = await fetchInitialFilters();
      console.log('Initial filter data:', data);
      setOptions(data);
    } catch (error) {
      console.error('Error fetching initial filters:', error);
      // If 401, logout user
      if (error.message.includes('401')) {
        handleLogout();
      }
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
      if (error.message.includes('401')) {
        handleLogout();
      }
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
      
      // Fetch all facility data (only permit_number, outfall, and date range)
      const facilityFilters = {
        permit_number: filters.permit_number,
        outfall: filters.outfall,
        startDate: filters.startDate,
        endDate: filters.endDate
      };
      
      const allDataResult = await fetchCombinedData(facilityFilters);
      setAllFacilityData(allDataResult.data || []);
      
    } catch (error) {
      console.error('Error fetching data:', error);
      setData([]);
      setAllFacilityData([]);
      setStatistics(null);
      if (error.message.includes('401')) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  // Show loading spinner while checking authentication
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Show login page if not authenticated
  if (!isAuthenticated) {
    return (
      <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
        <LoginPage onLogin={handleLogin} />
      </GoogleOAuthProvider>
    );
  }

  // Show main dashboard if authenticated
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
        {/* Top bar with user info and dark mode toggle */}
        <div className="flex justify-between items-center mb-4">
          <div className={`flex items-center gap-3 ${darkMode ? 'text-white' : 'text-gray-700'}`}>
            {user?.picture && (
              <img 
                src={user.picture} 
                alt={user.name} 
                className="w-8 h-8 rounded-full"
              />
            )}
            <span className="text-sm">{user?.name}</span>
            <button
              onClick={handleLogout}
              className={`text-sm px-3 py-1 rounded hover:bg-opacity-80 ${
                darkMode ? 'bg-gray-700 text-white' : 'bg-gray-200 text-gray-700'
              }`}
            >
              Logout
            </button>
          </div>
        </div>

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