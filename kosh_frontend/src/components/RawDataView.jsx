import React from 'react';

const RawDataView = ({ data }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Raw Data</h2>
      {data.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Outfall</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Parameter</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">DMR Value</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Unit</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Limit Value</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Limit Value</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Limit Value</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {data.map((row, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm text-gray-900">{row.monitoring_period_date}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.outfall_number}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.parameter_description}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.dmr_value}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.dmr_value_unit}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.limit_value}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.limit_value_unit}</td>
                  <td className="px-4 py-3 text-sm text-gray-900">{row.source_file_name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-500 text-center py-8">No data available. Please select filters and click Apply.</p>
      )}
    </div>
  );
};

export default RawDataView;