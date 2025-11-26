import React from 'react';

const RawDataView = ({ data, darkMode }) => {
  return (
    <div>
      <h2 className={`text-xl font-semibold mb-4 ${darkMode ? 'text-gray-100' : 'text-gray-800'}`}>
        Raw Data
      </h2>
      {data.length > 0 ? (
        <div className="overflow-x-auto">
          <table className={`min-w-full divide-y ${darkMode ? 'divide-gray-700' : 'divide-gray-200'}`}>
            <thead className={darkMode ? 'bg-gray-700' : 'bg-gray-50'}>
              <tr>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Date</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Outfall</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Parameter</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>DMR Value</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Unit</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Limit Value</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Limit Unit</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Source File</th>
              </tr>
            </thead>
            <tbody className={`divide-y ${darkMode ? 'bg-gray-800 divide-gray-700' : 'bg-white divide-gray-200'}`}>
              {data.map((row, idx) => (
                <tr key={idx} className={darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'}>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.monitoring_period_date}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.outfall_number}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.parameter_description}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.dmr_value}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.dmr_value_unit}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.limit_value}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.limit_value_unit}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.source_file_name}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className={`text-center py-8 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          No data available. Please select filters and click Apply.
        </p>
      )}
    </div>
  );
};

export default RawDataView;