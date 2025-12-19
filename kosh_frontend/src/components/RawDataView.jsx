import React from 'react';
import { Download } from 'lucide-react';
import ExcelJS from 'exceljs';

const RawDataView = ({ data, darkMode, filters }) => {
  const calculateStatistics = (rawData) => {
    print("Calculating statistics for raw data:", rawData);
    const values = rawData
      .map(item => parseFloat(item.value))
      .filter(val => !isNaN(val) && val !== null);
    
    if (values.length === 0) {
      return {
        count: 0,
        min: 0,
        max: 0,
        mean: 0,
        median: 0,
        std_dev: 0,
        variance: 0,
        skewness: 0,
        kurtosis: 0
      };
    }

    const count = values.length;
    const min = Math.min(...values);
    const max = Math.max(...values);
    const mean = values.reduce((a, b) => a + b, 0) / count;
    
    const sorted = [...values].sort((a, b) => a - b);
    const median = count % 2 === 0
      ? (sorted[count / 2 - 1] + sorted[count / 2]) / 2
      : sorted[Math.floor(count / 2)];
    
    const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / count;
    const std_dev = Math.sqrt(variance);
    
    const skewness = std_dev !== 0 
      ? values.reduce((sum, val) => sum + Math.pow((val - mean) / std_dev, 3), 0) / count
      : 0;
    
    const kurtosis = std_dev !== 0
      ? values.reduce((sum, val) => sum + Math.pow((val - mean) / std_dev, 4), 0) / count - 3
      : 0;
    
    return { count, min, max, mean, median, std_dev, variance, skewness, kurtosis };
  };

  const handleDownload = async () => {
    try {
      const workbook = new ExcelJS.Workbook();
      
      // Sheet 1: Raw Data
      const rawDataSheet = workbook.addWorksheet('Raw Data');
      rawDataSheet.columns = [
        { header: 'NPDES Permit Number', key: 'npdes_permit_number', width: 20 },
        { header: 'Outfall Number', key: 'outfall_number', width: 15 },
        { header: 'Monitoring Location Code', key: 'monitoring_location_code', width: 25 },
        { header: 'Limit Set Designator', key: 'limit_set_designator', width: 20 },
        { header: 'Parameter Code', key: 'parameter_code', width: 15 },
        { header: 'Parameter Description', key: 'parameter_description', width: 30 },
        { header: 'Monitoring Period Date', key: 'monitoring_period_date', width: 20 },
        { header: 'Limit Value', key: 'limit_value', width: 15 },
        { header: 'Limit Value Unit', key: 'limit_value_unit', width: 15 },
        { header: 'DMR Value Type', key: 'dmr_value_type', width: 15 },
        { header: 'Statistical Base', key: 'statistical_base', width: 15 },
        { header: 'Limit Type Code', key: 'limit_type_code', width: 15 },
        { header: 'DMR Value', key: 'dmr_value', width: 15 },
        { header: 'DMR Value Unit', key: 'dmr_value_unit', width: 15 },
        { header: 'DMR Comments', key: 'dmr_comments', width: 30 },
        { header: 'Source File Name', key: 'source_file_name', width: 30 },
        { header: 'Ingestion Timestamp', key: 'ingestion_timestamp', width: 20 }
      ];
      
      data.forEach(row => {
        rawDataSheet.addRow({
          npdes_permit_number: row.npdes_permit_number || '',
          outfall_number: row.outfall_number || '',
          monitoring_location_code: row.monitoring_location_code || '',
          limit_set_designator: row.limit_set_designator || '',
          parameter_code: row.parameter_code || '',
          parameter_description: row.parameter_description || '',
          monitoring_period_date: row.date || '',
          limit_value: row.limit_value || '',
          limit_value_unit: row.limit_value_unit || '',
          dmr_value_type: row.dmr_value_type || '',
          statistical_base: row.statistical_base || '',
          limit_type_code: row.limit_type_code || '',
          dmr_value: row.value || '',
          dmr_value_unit: row.dmr_value_unit || '',
          dmr_comments: row.dmr_comments || '',
          source_file_name: row.source_file_name || '',
          ingestion_timestamp: row.ingestion_timestamp || ''
        });
      });
      
      rawDataSheet.getRow(1).font = { bold: true };
      rawDataSheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FFE0E0E0' }
      };
      
      // Sheet 2: Chart Data
      const chartData = data.map(item => ({
        date: item.date || item.monitoring_period_date,
        value: parseFloat(item.value || item.dmr_value) || 0,
        limit: parseFloat(item.limit_value) || null
      }));

      const chartSheet = workbook.addWorksheet('Chart Data');
      chartSheet.columns = [
        { header: 'Date', key: 'date', width: 20 },
        { header: filters?.parameter || 'Value', key: 'value', width: 15 },
        { header: 'Limit Value', key: 'limit', width: 15 }
      ];
      
      chartData.forEach(item => {
        chartSheet.addRow({
          date: item.date,
          value: item.value,
          limit: item.limit !== null ? item.limit : ''
        });
      });
      
      chartSheet.getRow(1).font = { bold: true };
      chartSheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FFE0E0E0' }
      };
      
      // Sheet 3: Statistics
      const statsSheet = workbook.addWorksheet('Statistics');
      statsSheet.columns = [
        { header: 'Metric', key: 'metric', width: 25 },
        { header: 'Value', key: 'value', width: 20 }
      ];
      
      const stats = calculateStatistics(data);
      
      statsSheet.addRow({ metric: 'Count', value: stats.count });
      statsSheet.addRow({ metric: 'Minimum', value: stats.min.toFixed(2) });
      statsSheet.addRow({ metric: 'Maximum', value: stats.max.toFixed(2) });
      statsSheet.addRow({ metric: 'Mean', value: stats.mean.toFixed(2) });
      statsSheet.addRow({ metric: 'Median', value: stats.median.toFixed(2) });
      statsSheet.addRow({ metric: 'Standard Deviation', value: stats.std_dev.toFixed(2) });
      statsSheet.addRow({ metric: 'Variance', value: stats.variance.toFixed(2) });
      statsSheet.addRow({ metric: 'Skewness', value: stats.skewness.toFixed(2) });
      statsSheet.addRow({ metric: 'Kurtosis', value: stats.kurtosis.toFixed(2) });
      
      statsSheet.getRow(1).font = { bold: true };
      statsSheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FFE0E0E0' }
      };
      
      const buffer = await workbook.xlsx.writeBuffer();
      const blob = new Blob([buffer], { 
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${filters?.parameter || 'data'}_${new Date().toISOString().split('T')[0]}.xlsx`;
      link.click();
      URL.revokeObjectURL(url);
      
    } catch (error) {
      console.error('Error downloading file:', error);
      alert('Error downloading file. Please try again.');
    }
  };

  return (
    <div className="relative">
      {data.length > 0 && (
        <button
          onClick={handleDownload}
          className={`absolute top-0 right-0 p-2 rounded-md transition-all group ${
            darkMode 
              ? 'text-gray-400 hover:text-gray-200 hover:bg-gray-700' 
              : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
          }`}
          title="Download complete report"
        >
          <Download className="w-5 h-5" />
        </button>
      )}

      <h2 className={`text-xl font-semibold mb-4 pr-12 ${darkMode ? 'text-gray-100' : 'text-gray-800'}`}>
        Raw Data
      </h2>
      {data.length > 0 ? (
        <div className="overflow-x-auto">
          <table className={`min-w-full divide-y ${darkMode ? 'divide-gray-700' : 'divide-gray-200'}`}>
            <thead className={darkMode ? 'bg-gray-700' : 'bg-gray-50'}>
              <tr>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>NPDES Permit Number</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Outfall Number</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Monitoring Location Code</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Limit Set Designator</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Parameter Code</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Parameter Description</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Monitoring Period Date</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Limit Value</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Limit Value Unit</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>DMR Value Type</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Statistical Base</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Limit Type Code</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>DMR Value</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>DMR Value Unit</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>DMR Comments</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Source File Name</th>
                <th className={`px-4 py-3 text-left text-xs font-medium uppercase ${
                  darkMode ? 'text-gray-300' : 'text-gray-500'
                }`}>Ingestion Timestamp</th>
              </tr>
            </thead>
            <tbody className={`divide-y ${darkMode ? 'bg-gray-800 divide-gray-700' : 'bg-white divide-gray-200'}`}>
              {data.map((row, idx) => (
                <tr key={idx} className={darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-50'}>
                  
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.npdes_permit_number || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.outfall_number || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.monitoring_location_code || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.limit_set_designator || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.parameter_code || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.parameter_description || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.date || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.limit_value || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.limit_value_unit || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.dmr_value_type || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.statistical_base || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.limit_type_code || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.value || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.dmr_value_unit || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.dmr_comments || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.source_file_name || '-'}
                  </td>
                  <td className={`px-4 py-3 text-sm ${darkMode ? 'text-gray-300' : 'text-gray-900'}`}>
                    {row.ingestion_timestamp || '-'}
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