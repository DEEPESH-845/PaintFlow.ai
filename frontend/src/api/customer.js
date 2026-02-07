import api from './client'

export const fetchShades = (params) => api.get('/customer/shades', { params })
export const fetchShadeDetail = (id) => api.get(`/customer/shades/${id}`)
export const fetchShadeAvailability = (id, lat, lng) =>
  api.get(`/customer/shades/${id}/availability`, { params: { lat, lng } })
export const fetchNearbyDealers = (lat, lng) =>
  api.get('/customer/dealers/nearby', { params: { lat, lng } })
export const snapAndFind = (hexColor) =>
  api.post('/customer/snap-find', null, { params: { hex_color: hexColor } })
export const createOrderRequest = (data) => api.post('/customer/order-request', data)
