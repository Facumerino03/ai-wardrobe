import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Garments API
export const garmentAPI = {
  // Upload a new garment
  upload: async (formData) => {
    const response = await api.post('/api/garments/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get all garments
  getAll: async (userId = 'default_user') => {
    const response = await api.get(`/api/garments/?user_id=${userId}`);
    return response.data;
  },

  // Get single garment
  getById: async (id) => {
    const response = await api.get(`/api/garments/${id}`);
    return response.data;
  },

  // Search garments
  search: async (query, userId = 'default_user', filters = {}, nResults = 10) => {
    const response = await api.post('/api/garments/search', {
      query,
      user_id: userId,
      filters,
      n_results: nResults,
    });
    return response.data;
  },

  // Update garment
  update: async (id, data) => {
    const response = await api.put(`/api/garments/${id}`, data);
    return response.data;
  },

  // Delete garment
  delete: async (id) => {
    const response = await api.delete(`/api/garments/${id}`);
    return response.data;
  },

  // Get image URL
  getImageUrl: (filename) => {
    return `${API_BASE_URL}/api/garments/images/${filename}`;
  },
};

// Outfits API
export const outfitAPI = {
  // Create outfit
  create: async (data) => {
    const response = await api.post('/api/outfits/', data);
    return response.data;
  },

  // Get all outfits
  getAll: async (userId = 'default_user') => {
    const response = await api.get(`/api/outfits/?user_id=${userId}`);
    return response.data;
  },

  // Get single outfit
  getById: async (id) => {
    const response = await api.get(`/api/outfits/${id}`);
    return response.data;
  },

  // Get AI suggestions
  suggest: async (query, userId = 'default_user', context = {}) => {
    const response = await api.post('/api/outfits/suggest', {
      query,
      user_id: userId,
      context,
    });
    return response.data;
  },

  // Update outfit
  update: async (id, data) => {
    const response = await api.put(`/api/outfits/${id}`, data);
    return response.data;
  },

  // Delete outfit
  delete: async (id) => {
    const response = await api.delete(`/api/outfits/${id}`);
    return response.data;
  },

  // Rate outfit
  rate: async (id, rating) => {
    const response = await api.post(`/api/outfits/${id}/rate`, { rating });
    return response.data;
  },
};

// Chat API
export const chatAPI = {
  // Send message
  sendMessage: async (message, userId = 'default_user', sessionId = 'default_session', context = {}) => {
    const response = await api.post('/api/chat/message', {
      message,
      user_id: userId,
      session_id: sessionId,
      context,
    });
    return response.data;
  },

  // Get conversation history
  getHistory: async (sessionId, userId = 'default_user') => {
    const response = await api.get(`/api/chat/history/${sessionId}?user_id=${userId}`);
    return response.data;
  },

  // Clear conversation
  clear: async (sessionId, userId = 'default_user') => {
    const response = await api.delete(`/api/chat/clear/${sessionId}?user_id=${userId}`);
    return response.data;
  },
};

// Virtual Try-On API
export const tryonAPI = {
  // Generate try-on
  generate: async (formData) => {
    const response = await api.post('/api/tryon/generate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Check API health
  checkHealth: async () => {
    const response = await api.get('/api/tryon/health');
    return response.data;
  },

  // Get generated image URL
  getImageUrl: (filename) => {
    return `${API_BASE_URL}/api/tryon/images/${filename}`;
  },
};

export default api;
