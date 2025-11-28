const API_BASE = 'https://kosh-backend-569071530463.europe-west1.run.app';
// const API_BASE = 'http://127.0.0.1:8080/';

// Filter APIs - Now include both NPDES and Weather data
export const fetchInitialFilters = async () => {
  const response = await fetch(`${API_BASE}/api/filters/initial`);
  return response.json();
};

export const fetchCascadingFilters = async (filters) => {
  const response = await fetch(`${API_BASE}/api/filters/cascading`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(filters)
  });
  return response.json();
};

// Legacy NPDES-only endpoints (keep for backward compatibility if needed)
export const fetchData = async (filters) => {
  const params = new URLSearchParams();
  if (filters.outfall) params.append('outfall', filters.outfall);
  if (filters.parameter) params.append('parameter', filters.parameter);
  if (filters.base) params.append('base', filters.base);
  if (filters.unit) params.append('unit', filters.unit);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);

  const response = await fetch(`${API_BASE}/data?${params}`);
  return response.json();
};

export const fetchStatistics = async (filters) => {
  const params = new URLSearchParams();
  if (filters.outfall) params.append('outfall', filters.outfall);
  if (filters.parameter) params.append('parameter', filters.parameter);
  if (filters.base) params.append('base', filters.base);
  if (filters.unit) params.append('unit', filters.unit);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);

  const response = await fetch(`${API_BASE}/api/data/statistics?${params}`);
  return response.json();
};

// NEW: Combined NPDES + Weather endpoints
export const fetchCombinedData = async (filters) => {
  const params = new URLSearchParams();
  if (filters.outfall) params.append('outfall', filters.outfall);
  if (filters.parameter) params.append('parameter', filters.parameter);
  if (filters.base) params.append('base', filters.base);
  if (filters.unit) params.append('unit', filters.unit);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);
  if (filters.limit) params.append('limit', filters.limit);

  const response = await fetch(`${API_BASE}/api/data/combined?${params}`);
  return response.json();
};

export const fetchCombinedStatistics = async (filters) => {
  const params = new URLSearchParams();
  if (filters.outfall) params.append('outfall', filters.outfall);
  if (filters.parameter) params.append('parameter', filters.parameter);
  if (filters.base) params.append('base', filters.base);
  if (filters.unit) params.append('unit', filters.unit);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);

  const response = await fetch(`${API_BASE}/api/data/statistics/combined?${params}`);
  return response.json();
};