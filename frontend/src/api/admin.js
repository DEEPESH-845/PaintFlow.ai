import api from './client'

export const fetchDashboardSummary = () => api.get('/admin/dashboard/summary')
export const fetchInventoryMap = () => api.get('/admin/inventory/map')
export const fetchWarehouseInventory = (id) => api.get(`/admin/inventory/warehouse/${id}`)
export const fetchDeadStock = () => api.get('/admin/dead-stock')
export const fetchTransfers = () => api.get('/admin/transfers/recommended')
export const approveTransfer = (id) => api.post(`/admin/transfers/${id}/approve`)
export const autoBalance = (id) => api.post(`/admin/transfers/${id}/auto-balance`)
export const fetchDealerPerformance = (regionId) =>
  api.get('/admin/dealers/performance', { params: regionId ? { region_id: regionId } : {} })
export const fetchTopSkus = (limit = 10) => api.get('/admin/top-skus', { params: { limit } })
