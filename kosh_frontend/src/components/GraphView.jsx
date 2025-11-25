import React, { useRef } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Download } from 'lucide-react';
import ExcelJS from 'exceljs';

const GraphView = ({ data, filters }) => {
  const chartRef = useRef(null);

  const chartData = data.map(item => ({
    date: item.monitoring_period_date,
    value: parseFloat(item.dmr_value) || 0,
    limit: parseFloat(item.limit_value) || null
  }));

  // Use parameter name in title, or default text
  const chartTitle = filters?.parameter 
    ? `${filters.parameter} Over Time` 
    : 'DMR Values Over Time';

  const handleDownload = async () => {
    try {
      // Create a new workbook
      const workbook = new ExcelJS.Workbook();
      
      // Sheet 1: Data Table
      const dataSheet = workbook.addWorksheet('Data');
      
      // Add headers
      dataSheet.columns = [
        { header: 'Date', key: 'date', width: 15 },
        { header: `${filters?.parameter || 'DMR Value'}`, key: 'value', width: 20 },
        { header: 'Limit Value', key: 'limit', width: 20 }
      ];
      
      // Add data rows
      chartData.forEach(item => {
        dataSheet.addRow({
          date: item.date,
          value: item.value,
          limit: item.limit !== null ? item.limit : 'N/A'
        });
      });
      
      // Style the header row
      dataSheet.getRow(1).font = { bold: true };
      dataSheet.getRow(1).fill = {
        type: 'pattern',
        pattern: 'solid',
        fgColor: { argb: 'FFE0E0E0' }
      };
      
      // Sheet 2: Chart Image
      const chartSheet = workbook.addWorksheet('Chart');
      
      // Get the chart SVG
      const chartContainer = chartRef.current;
      if (chartContainer) {
        const svgElement = chartContainer.querySelector('svg');
        if (svgElement) {
          // Create canvas and convert SVG to PNG
          const canvas = document.createElement('canvas');
          const ctx = canvas.getContext('2d');
          const svgString = new XMLSerializer().serializeToString(svgElement);
          const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
          const url = URL.createObjectURL(svgBlob);
          const img = new Image();
          
          await new Promise((resolve, reject) => {
            img.onload = async () => {
              canvas.width = svgElement.width.baseVal.value;
              canvas.height = svgElement.height.baseVal.value;
              
              // Fill white background
              ctx.fillStyle = 'white';
              ctx.fillRect(0, 0, canvas.width, canvas.height);
              ctx.drawImage(img, 0, 0);
              
              // Convert canvas to base64
              canvas.toBlob(async (blob) => {
                const reader = new FileReader();
                reader.onloadend = async () => {
                  const base64Image = reader.result.split(',')[1];
                  
                  // Add image to Excel
                  const imageId = workbook.addImage({
                    base64: base64Image,
                    extension: 'png',
                  });
                  
                  chartSheet.addImage(imageId, {
                    tl: { col: 0, row: 0 },
                    ext: { width: canvas.width, height: canvas.height }
                  });
                  
                  // Generate and download Excel file
                  const buffer = await workbook.xlsx.writeBuffer();
                  const blob = new Blob([buffer], { 
                    type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
                  });
                  const downloadUrl = URL.createObjectURL(blob);
                  const link = document.createElement('a');
                  link.href = downloadUrl;
                  link.download = `${filters?.parameter || 'dmr_data'}_${new Date().toISOString().split('T')[0]}.xlsx`;
                  link.click();
                  URL.revokeObjectURL(downloadUrl);
                  
                  resolve();
                };
                reader.readAsDataURL(blob);
              });
              
              URL.revokeObjectURL(url);
            };
            img.onerror = reject;
            img.src = url;
          });
        }
      }
      
    } catch (error) {
      console.error('Error downloading file:', error);
      alert('Error downloading file. Please try again.');
    }
  };

  return (
    <div className="relative">
      {/* Download Button */}
      {chartData.length > 0 && (
        <button
          onClick={handleDownload}
          className="absolute top-0 right-0 p-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md shadow-sm transition-colors flex items-center gap-1 text-sm z-10"
          title="Download chart and data"
        >
          <Download className="w-4 h-4" />
          <span className="hidden sm:inline">Download</span>
        </button>
      )}

      <h2 className="text-xl font-semibold text-gray-800 mb-4 pr-32">{chartTitle}</h2>
      {console.log('GraphView data:', chartData)}
      {chartData.length > 0 ? (
        <div ref={chartRef}>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="value" stroke="#3b82f6" name={filters?.parameter || "DMR Value"} />
              {chartData.some(d => d.limit !== null) && (
                <Line type="monotone" dataKey="limit" stroke="#ef4444" name="Limit Value" strokeDasharray="5 5" />
              )}
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <p className="text-gray-500 text-center py-8">No data available. Please select filters and click Apply.</p>
      )}
    </div>
  );
};

export default GraphView;