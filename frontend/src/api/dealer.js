import api from './client'

export const fetchDealerDashboard = (id) => api.get(`/dealer/${id}/dashboard`)
export const fetchSmartOrders = (id) => api.get(`/dealer/${id}/smart-orders`)
export const placeOrder = (id, data) => api.post(`/dealer/${id}/orders`, data)
export const acceptBundle = (id) => api.post(`/dealer/${id}/orders/bundle`)
export const fetchOrders = (id) => api.get(`/dealer/${id}/orders`)
export const fetchDealerAlerts = (id) => api.get(`/dealer/${id}/alerts`)
