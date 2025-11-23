const API_BASE = 'http://localhost:8080';

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