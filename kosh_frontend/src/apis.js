const API_BASE = import.meta.env.VITE_BACKEND_URL;

// Helper function to get JWT token from localStorage
const getAuthHeaders = () => {
  const token = localStorage.getItem('jwt_token');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

// Helper function to handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    if (response.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('jwt_token');
      localStorage.removeItem('user_info');
      throw new Error('401: Authentication required');
    }
    const error = await response.json().catch(() => ({ error: 'Request failed' }));
    throw new Error(error.error || 'API request failed');
  }
  return response.json();
};

// Filter APIs - Now include NPDES permit number, outfalls, and Weather data
export const fetchInitialFilters = async () => {
  const response = await fetch(`${API_BASE}/api/filters/initial`, {
    headers: getAuthHeaders()
  });
  return handleResponse(response);
};

export const fetchCascadingFilters = async (filters) => {
  const response = await fetch(`${API_BASE}/api/filters/cascading`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(filters)
  });
  return handleResponse(response);
};

// Legacy NPDES-only endpoints (keep for backward compatibility if needed)
export const fetchData = async (filters) => {
  const params = new URLSearchParams();
  if (filters.permit_number) params.append('permit_number', filters.permit_number);
  if (filters.outfall) params.append('outfall', filters.outfall);
  if (filters.parameter) params.append('parameter', filters.parameter);
  if (filters.base) params.append('base', filters.base);
  if (filters.unit) params.append('unit', filters.unit);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);

  const response = await fetch(`${API_BASE}/data?${params}`, {
    headers: getAuthHeaders()
  });
  return handleResponse(response);
};

export const fetchStatistics = async (filters) => {
  const params = new URLSearchParams();
  if (filters.permit_number) params.append('permit_number', filters.permit_number);
  if (filters.outfall) params.append('outfall', filters.outfall);
  if (filters.parameter) params.append('parameter', filters.parameter);
  if (filters.base) params.append('base', filters.base);
  if (filters.unit) params.append('unit', filters.unit);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);

  const response = await fetch(`${API_BASE}/api/data/statistics?${params}`, {
    headers: getAuthHeaders()
  });
  return handleResponse(response);
};

// Combined NPDES + Weather endpoints
export const fetchCombinedData = async (filters) => {
  const params = new URLSearchParams();
  if (filters.permit_number) params.append('permit_number', filters.permit_number);
  if (filters.outfall) params.append('outfall', filters.outfall);
  if (filters.parameter) params.append('parameter', filters.parameter);
  if (filters.base) params.append('base', filters.base);
  if (filters.unit) params.append('unit', filters.unit);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);
  if (filters.limit) params.append('limit', filters.limit);

  const response = await fetch(`${API_BASE}/api/data/combined?${params}`, {
    headers: getAuthHeaders()
  });
  return handleResponse(response);
};

export const fetchCombinedStatistics = async (filters) => {
  const params = new URLSearchParams();
  if (filters.permit_number) params.append('permit_number', filters.permit_number);
  if (filters.outfall) params.append('outfall', filters.outfall);
  if (filters.parameter) params.append('parameter', filters.parameter);
  if (filters.base) params.append('base', filters.base);
  if (filters.unit) params.append('unit', filters.unit);
  if (filters.startDate) params.append('start_date', filters.startDate);
  if (filters.endDate) params.append('end_date', filters.endDate);

  const response = await fetch(`${API_BASE}/api/data/statistics/combined?${params}`, {
    headers: getAuthHeaders()
  });
  return handleResponse(response);
};