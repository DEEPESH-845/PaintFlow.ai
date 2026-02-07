import api from './client'

export const fetchForecast = (skuId, regionId = 1, horizon = 30) =>
  api.get(`/forecast/${skuId}`, { params: { region_id: regionId, horizon } })
export const fetchRegionalSummary = () => api.get('/forecast/regional/summary')
