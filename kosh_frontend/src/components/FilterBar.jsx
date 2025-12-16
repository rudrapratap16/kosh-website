import React, { useState, useRef, useEffect } from 'react';
import { ChevronLeft, ChevronRight, ChevronDown, Search, X, Calendar } from 'lucide-react';

const SearchableSelect = ({ value, options, onChange, placeholder, darkMode, label }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const dropdownRef = useRef(null);

  const filteredOptions = options.filter(option =>
    option.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
        setSearchTerm('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (option) => {
    onChange(option);
    setIsOpen(false);
    setSearchTerm('');
  };

  const handleClear = () => {
    onChange('');
    setSearchTerm('');
  };

  return (
    <div ref={dropdownRef} className="relative">
      <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
        {label}
      </label>
      <div
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full px-3 py-2 border rounded-md cursor-pointer flex items-center justify-between ${
          darkMode 
            ? 'bg-gray-700 border-gray-600 text-gray-100 hover:bg-gray-650' 
            : 'bg-white border-gray-300 text-gray-900 hover:bg-gray-50'
        }`}
      >
        <span className={value ? '' : 'text-gray-500'}>
          {value || placeholder}
        </span>
        <div className="flex items-center gap-2">
          {value && (
            <X
              className="w-4 h-4 text-gray-400 hover:text-gray-600"
              onClick={(e) => {
                e.stopPropagation();
                handleClear();
              }}
            />
          )}
          <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </div>
      </div>

      {isOpen && (
        <div className={`absolute z-50 w-full mt-1 border rounded-md shadow-lg max-h-60 overflow-hidden ${
          darkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-300'
        }`}>
          <div className={`p-2 border-b ${darkMode ? 'border-gray-600' : 'border-gray-200'}`}>
            <div className={`flex items-center gap-2 px-3 py-2 rounded-md ${
              darkMode ? 'bg-gray-600' : 'bg-gray-100'
            }`}>
              <Search className="w-4 h-4 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search..."
                className={`flex-1 bg-transparent outline-none ${
                  darkMode ? 'text-gray-100 placeholder-gray-400' : 'text-gray-900 placeholder-gray-500'
                }`}
                onClick={(e) => e.stopPropagation()}
              />
            </div>
          </div>
          <div className="overflow-y-auto max-h-48">
            {filteredOptions.length > 0 ? (
              filteredOptions.map((option) => (
                <div
                  key={option}
                  onClick={() => handleSelect(option)}
                  className={`px-3 py-2 cursor-pointer transition-colors ${
                    value === option
                      ? darkMode
                        ? 'bg-blue-900/50 text-blue-300'
                        : 'bg-blue-50 text-blue-600'
                      : darkMode
                        ? 'hover:bg-gray-600 text-gray-100'
                        : 'hover:bg-gray-100 text-gray-900'
                  }`}
                >
                  {option}
                </div>
              ))
            ) : (
              <div className={`px-3 py-2 text-center ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                No results found
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

const CustomDatePicker = ({ value, onChange, label, darkMode }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedDate, setSelectedDate] = useState(value ? new Date(value) : null);
  const [currentMonth, setCurrentMonth] = useState(value ? new Date(value) : new Date());
  const dropdownRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    if (value) {
      const date = new Date(value);
      setSelectedDate(date);
      setCurrentMonth(date);
    }
  }, [value]);

  const daysInMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const firstDayOfMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  };

  const handleDateClick = (day) => {
    const newDate = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day);
    setSelectedDate(newDate);
    const formattedDate = newDate.toISOString().split('T')[0];
    onChange(formattedDate);
    setIsOpen(false);
  };

  const handlePrevMonth = () => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1));
  };

  const handleNextMonth = () => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1));
  };

  const handleMonthChange = (e) => {
    setCurrentMonth(new Date(currentMonth.getFullYear(), parseInt(e.target.value)));
  };

  const handleYearChange = (e) => {
    setCurrentMonth(new Date(parseInt(e.target.value), currentMonth.getMonth()));
  };

  const handleClear = (e) => {
    e.stopPropagation();
    setSelectedDate(null);
    onChange('');
  };

  const generateYearOptions = () => {
    const currentYear = new Date().getFullYear();
    const years = [];
    for (let i = currentYear - 100; i <= currentYear + 10; i++) {
      years.push(i);
    }
    return years;
  };

  const renderCalendar = () => {
    const days = daysInMonth(currentMonth);
    const firstDay = firstDayOfMonth(currentMonth);
    const calendarDays = [];

    // Previous month's days (grayed out)
    const prevMonthDays = firstDay;
    const prevMonth = new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1);
    const prevMonthTotal = daysInMonth(prevMonth);
    
    for (let i = prevMonthTotal - prevMonthDays + 1; i <= prevMonthTotal; i++) {
      calendarDays.push(
        <div
          key={`prev-${i}`}
          className={`p-2 text-center text-sm ${
            darkMode ? 'text-gray-600' : 'text-gray-400'
          } opacity-40`}
        >
          {i}
        </div>
      );
    }

    // Current month's days
    for (let day = 1; day <= days; day++) {
      const isSelected = selectedDate && 
        selectedDate.getDate() === day && 
        selectedDate.getMonth() === currentMonth.getMonth() &&
        selectedDate.getFullYear() === currentMonth.getFullYear();
      
      const isToday = new Date().getDate() === day && 
        new Date().getMonth() === currentMonth.getMonth() &&
        new Date().getFullYear() === currentMonth.getFullYear();

      calendarDays.push(
        <div
          key={day}
          onClick={() => handleDateClick(day)}
          className={`p-2 text-center text-sm cursor-pointer rounded-lg transition-colors ${
            isSelected
              ? 'bg-blue-600 text-white font-semibold'
              : isToday
              ? darkMode
                ? 'bg-gray-600 text-gray-100 font-medium'
                : 'bg-gray-200 text-gray-900 font-medium'
              : darkMode
              ? 'text-gray-100 hover:bg-gray-600'
              : 'text-gray-900 hover:bg-gray-100'
          }`}
        >
          {day}
        </div>
      );
    }

    // Next month's days (grayed out)
    const remainingDays = 42 - calendarDays.length;
    for (let i = 1; i <= remainingDays; i++) {
      calendarDays.push(
        <div
          key={`next-${i}`}
          className={`p-2 text-center text-sm ${
            darkMode ? 'text-gray-600' : 'text-gray-400'
          } opacity-40`}
        >
          {i}
        </div>
      );
    }

    return calendarDays;
  };

  const formatDisplayDate = () => {
    if (!selectedDate) return '';
    return selectedDate.toISOString().split('T')[0];
  };

  return (
    <div ref={dropdownRef} className="relative">
      <label className={`block text-sm font-medium mb-2 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
        {label}
      </label>
      <div className="relative">
        <div
          onClick={() => setIsOpen(!isOpen)}
          className={`w-full px-3 py-2 pr-10 border rounded-md cursor-pointer flex items-center justify-between ${
            darkMode 
              ? 'bg-gray-700 border-gray-600 text-gray-100 hover:bg-gray-650' 
              : 'bg-white border-gray-300 text-gray-900 hover:bg-gray-50'
          }`}
        >
          <span className={formatDisplayDate() ? '' : 'text-gray-500'}>
            {formatDisplayDate() || 'Select date'}
          </span>
          <div className="flex items-center gap-2">
            {selectedDate && (
              <X
                className="w-4 h-4 text-gray-400 hover:text-gray-600"
                onClick={handleClear}
              />
            )}
          </div>
        </div>
        <Calendar className={`absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none ${
          darkMode ? 'text-gray-400' : 'text-gray-500'
        }`} />
      </div>

      {isOpen && (
        <div className={`absolute z-50 w-full mt-1 border rounded-lg shadow-lg p-4 ${
          darkMode ? 'bg-gray-700 border-gray-600' : 'bg-white border-gray-300'
        }`}>
          {/* Header */}
          <div className="flex items-center justify-between mb-4 gap-2">
            <button
              onClick={handlePrevMonth}
              className={`p-1 rounded hover:bg-opacity-80 transition-colors flex-shrink-0 ${
                darkMode ? 'hover:bg-gray-600' : 'hover:bg-gray-100'
              }`}
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <div className="flex gap-2 flex-1 justify-center">
              <select
                value={currentMonth.getMonth()}
                onChange={handleMonthChange}
                className={`px-2 py-1 rounded border text-sm font-semibold cursor-pointer ${
                  darkMode 
                    ? 'bg-gray-600 border-gray-500 text-gray-100' 
                    : 'bg-white border-gray-300 text-gray-900'
                }`}
              >
                {['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December'].map((month, idx) => (
                  <option key={month} value={idx}>{month}</option>
                ))}
              </select>
              <select
                value={currentMonth.getFullYear()}
                onChange={handleYearChange}
                className={`px-2 py-1 rounded border text-sm font-semibold cursor-pointer ${
                  darkMode 
                    ? 'bg-gray-600 border-gray-500 text-gray-100' 
                    : 'bg-white border-gray-300 text-gray-900'
                }`}
              >
                {generateYearOptions().map((year) => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>
            <button
              onClick={handleNextMonth}
              className={`p-1 rounded hover:bg-opacity-80 transition-colors flex-shrink-0 ${
                darkMode ? 'hover:bg-gray-600' : 'hover:bg-gray-100'
              }`}
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>

          {/* Day names */}
          <div className="grid grid-cols-7 gap-1 mb-2">
            {['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'].map((day) => (
              <div
                key={day}
                className={`text-center text-xs font-semibold p-2 ${
                  darkMode ? 'text-gray-400' : 'text-gray-600'
                }`}
              >
                {day}
              </div>
            ))}
          </div>

          {/* Calendar days */}
          <div className="grid grid-cols-7 gap-1">
            {renderCalendar()}
          </div>
        </div>
      )}
    </div>
  );
};

const FilterBar = ({ filters, options, onFilterChange, onDateChange, onApply, loading, onCollapseChange, darkMode }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const safeOptions = {
    permit_numbers: options?.permit_numbers || [],
    outfalls: options?.outfalls || [],
    parameters: options?.parameters || [],
    bases: options?.bases || [],
    units: options?.units || []
  };

  return (
    <div 
      className={`fixed left-0 top-0 h-full shadow-lg transition-all duration-300 z-10 group ${
        isCollapsed ? 'w-12' : 'w-80'
      } ${darkMode ? 'bg-gray-800' : 'bg-white'}`}
    >
      <button
        onClick={() => {
          setIsCollapsed(!isCollapsed);
          onCollapseChange?.(!isCollapsed);
        }}
        className={`absolute right-2 top-6 rounded p-2 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 ${
          darkMode 
            ? 'bg-gray-700 hover:bg-gray-600 text-gray-300' 
            : 'bg-gray-100 hover:bg-gray-200 text-gray-600'
        }`}
      >
        {isCollapsed ? (
          <ChevronRight className="w-4 h-4" />
        ) : (
          <ChevronLeft className="w-4 h-4" />
        )}
      </button>

      <div className={`h-full overflow-y-auto p-6 pt-16 ${isCollapsed ? 'invisible' : 'visible'}`}>
        <div className="space-y-4">
          <SearchableSelect
            value={filters.permit_number}
            options={safeOptions.permit_numbers}
            onChange={(value) => onFilterChange('permit_number', value)}
            placeholder="Select Station"
            darkMode={darkMode}
            label="Station Name"
          />

          <SearchableSelect
            value={filters.outfall}
            options={safeOptions.outfalls}
            onChange={(value) => onFilterChange('outfall', value)}
            placeholder="Select Outfall"
            darkMode={darkMode}
            label="Outfall"
          />

          <SearchableSelect
            value={filters.parameter}
            options={safeOptions.parameters}
            onChange={(value) => onFilterChange('parameter', value)}
            placeholder="Select Parameter"
            darkMode={darkMode}
            label="Parameters"
          />

          <SearchableSelect
            value={filters.base}
            options={safeOptions.bases}
            onChange={(value) => onFilterChange('base', value)}
            placeholder="Select Base"
            darkMode={darkMode}
            label="Base"
          />

          <SearchableSelect
            value={filters.unit}
            options={safeOptions.units}
            onChange={(value) => onFilterChange('unit', value)}
            placeholder="Select Unit"
            darkMode={darkMode}
            label="Unit"
          />

          <CustomDatePicker
            value={filters.startDate}
            onChange={(value) => onDateChange('startDate', value)}
            label="Start Date"
            darkMode={darkMode}
          />

          <CustomDatePicker
            value={filters.endDate}
            onChange={(value) => onDateChange('endDate', value)}
            label="End Date"
            darkMode={darkMode}
          />
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