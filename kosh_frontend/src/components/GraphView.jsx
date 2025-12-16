import React, { useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Download } from 'lucide-react';
import ExcelJS from 'exceljs';

const GraphView = ({ data, filters, darkMode }) => {
  const chartRef = useRef(null);

  const chartData = data.map(item => ({
    date: item.date || item.monitoring_period_date,
    value: parseFloat(item.value || item.dmr_value) || 0,
    dataSource: item.data_source
  }));

  const chartTitle = filters?.parameter 
    ? `${filters.parameter} Over Time` 
    : 'Values Over Time';

  const calculateStatistics = (rawData) => {
    const values = rawData
      .map(item => parseFloat(item.dmr_value))
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
          monitoring_period_date: row.monitoring_period_date || '',
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
        value: parseFloat(item.value || item.dmr_value) || 0
      }));

      const chartSheet = workbook.addWorksheet('Chart Data');
      chartSheet.columns = [
        { header: 'Date', key: 'date', width: 20 },
        { header: filters?.parameter || 'Value', key: 'value', width: 15 }
      ];
      
      chartData.forEach(item => {
        chartSheet.addRow({
          date: item.date,
          value: item.value
        });
      });
      
      chartSheet.getRow(1).font = { bold: true };
      chartSheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FFE0E0E0' }
      };
      
      // Add chart to Chart Data sheet
      chartSheet.addImage({
        image: workbook.addImage({
          base64: '', // We'll create a chart using Excel's native charting
          extension: 'png',
        }),
        tl: { col: 4, row: 1 },
        ext: { width: 600, height: 400 }
      });
      
      // Add chart using worksheet chart support
      const dataRowCount = chartData.length;
      
      // Create the chart (Note: ExcelJS has limited chart support, but we can add chart XML)
      chartSheet.addChart = {
        type: 'line',
        name: `${filters?.parameter || 'Parameter'} Over Time`,
        position: 'E2:N22',
        series: [
          {
            name: filters?.parameter || 'Value',
            categories: `'Chart Data'!$A$2:$A$${dataRowCount + 1}`,
            values: `'Chart Data'!$B$2:$B$${dataRowCount + 1}`,
          }
        ],
        axes: {
          category: { title: 'Date' },
          value: { title: filters?.parameter || 'Value' }
        }
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
      {chartData.length > 0 && (
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
        {chartTitle}
      </h2>
      {chartData.length > 0 ? (
        <div ref={chartRef}>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? '#374151' : '#e5e7eb'} />
              <XAxis 
                dataKey="date" 
                stroke={darkMode ? '#9ca3af' : '#6b7280'}
              />
              <YAxis stroke={darkMode ? '#9ca3af' : '#6b7280'} />
              <Tooltip 
                contentStyle={{
                  backgroundColor: darkMode ? '#1f2937' : '#ffffff',
                  border: `1px solid ${darkMode ? '#374151' : '#e5e7eb'}`,
                  color: darkMode ? '#f3f4f6' : '#111827'
                }}
              />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#3b82f6" name={filters?.parameter || "Value"} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <p className={`text-center py-8 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
          No data available. Please select filters and click Apply.
        </p>
      )}
    </div>
  );
};

export default GraphView;