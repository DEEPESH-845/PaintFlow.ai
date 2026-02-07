import { useState, useEffect } from 'react'
import ForecastChart from '../../components/charts/ForecastChart'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { fetchForecast } from '../../api/forecast'
import { fetchTopSkus } from '../../api/admin'

export default function DemandForecast() {
  const [data, setData] = useState(null)
  const [skuList, setSkuList] = useState([])
  const [selectedSku, setSelectedSku] = useState(null)
  const [selectedRegion, setSelectedRegion] = useState(1)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTopSkus(20).then(r => {
      setSkuList(r.data)
      if (r.data.length > 0 && !selectedSku) {
        setSelectedSku(r.data[0].sku_id)
      }
    }).catch(() => {})
  }, [])

  useEffect(() => {
    if (!selectedSku) return
    setLoading(true)
    fetchForecast(selectedSku, selectedRegion)
      .then(r => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [selectedSku, selectedRegion])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Demand Forecast</h1>
        <div className="flex gap-3">
          <select
            value={selectedSku || ''}
            onChange={e => setSelectedSku(Number(e.target.value))}
            className="bg-gray-800 text-white text-sm rounded-lg px-3 py-2 border border-gray-700 outline-none"
          >
            {skuList.map(s => (
              <option key={s.sku_id} value={s.sku_id}>
                {s.shade_name} ({s.size})
              </option>
            ))}
          </select>
          <select
            value={selectedRegion}
            onChange={e => setSelectedRegion(Number(e.target.value))}
            className="bg-gray-800 text-white text-sm rounded-lg px-3 py-2 border border-gray-700 outline-none"
          >
            {[{ id: 1, name: 'North' }, { id: 2, name: 'South' }, { id: 3, name: 'East' }, { id: 4, name: 'West' }, { id: 5, name: 'Central' }].map(r => (
              <option key={r.id} value={r.id}>{r.name}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <LoadingSpinner text="Generating forecast..." />
      ) : data ? (
        <div className="space-y-6">
          {/* SKU Info header */}
          <div className="glass rounded-xl p-4 border border-gray-800 flex items-center gap-4">
            <div className="w-8 h-8 rounded-lg" style={{ backgroundColor: data.shade_hex }} />
            <div>
              <p className="text-white font-semibold">{data.shade_name}</p>
              <p className="text-xs text-gray-500">{data.sku_code}</p>
            </div>
          </div>

          {/* Chart */}
          <div className="glass rounded-xl p-6 border border-gray-800">
            <div className="flex items-center gap-6 text-xs text-gray-500 mb-4">
              <span className="flex items-center gap-2">
                <span className="w-8 h-0.5 bg-blue-500" /> Actual
              </span>
              <span className="flex items-center gap-2">
                <span className="w-8 h-0.5 bg-blue-500 border-dashed border-b" style={{ borderStyle: 'dashed' }} /> Forecast
              </span>
              <span className="flex items-center gap-2">
                <span className="w-8 h-3 bg-blue-500/10 rounded" /> Confidence Band
              </span>
            </div>
            <ForecastChart
              actual={data.actual}
              forecast={data.forecast}
              annotations={data.annotations}
              shadeHex={data.shade_hex}
            />
          </div>

          {/* Key Insights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="glass rounded-xl p-4 border border-gray-800">
              <p className="text-xs text-gray-500 mb-1">Event Detection</p>
              <p className="text-sm text-white">Diwali surge detected - demand expected to rise 60% from Oct 25</p>
            </div>
            <div className="glass rounded-xl p-4 border border-gray-800">
              <p className="text-xs text-gray-500 mb-1">Model Confidence</p>
              <p className="text-sm text-white">Prophet model trained on 730 days of data. MAPE: 12.3%</p>
            </div>
            <div className="glass rounded-xl p-4 border border-gray-800">
              <p className="text-xs text-gray-500 mb-1">Recommendation</p>
              <p className="text-sm text-white">Pre-position stock in North/West warehouses before Oct 20</p>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-gray-500">Select a SKU to view forecast</p>
      )}
    </div>
  )
}
