import { useState, useEffect } from 'react'
import DataTable from '../../components/common/DataTable'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import AlertBadge from '../../components/common/AlertBadge'
import { fetchDealerPerformance } from '../../api/admin'
import { formatCurrency } from '../../utils/formatters'

const tierColors = {
  Platinum: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  Gold: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  Silver: 'bg-gray-500/20 text-gray-300 border-gray-500/30',
}

export default function DealerPerformance() {
  const [dealers, setDealers] = useState([])
  const [loading, setLoading] = useState(true)
  const [regionFilter, setRegionFilter] = useState('')

  useEffect(() => {
    setLoading(true)
    fetchDealerPerformance(regionFilter || null)
      .then(r => setDealers(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [regionFilter])

  const columns = [
    {
      key: 'name',
      label: 'Dealer',
      render: (v, row) => (
        <div>
          <p className="text-white font-medium">{v}</p>
          <p className="text-[10px] text-gray-500">{row.code} | {row.city}, {row.state}</p>
        </div>
      ),
    },
    {
      key: 'tier',
      label: 'Tier',
      render: v => (
        <span className={`inline-flex px-2 py-0.5 rounded-full text-[10px] font-semibold border ${tierColors[v] || tierColors.Silver}`}>
          {v}
        </span>
      ),
    },
    {
      key: 'performance_score',
      label: 'Score',
      render: v => (
        <div className="flex items-center gap-2">
          <div className="w-16 h-1.5 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full rounded-full"
              style={{
                width: `${v}%`,
                background: v >= 70 ? '#10b981' : v >= 40 ? '#f59e0b' : '#ef4444',
              }}
            />
          </div>
          <span className="text-xs font-mono text-white">{v?.toFixed(1)}</span>
        </div>
      ),
    },
    { key: 'total_orders', label: 'Orders' },
    {
      key: 'total_revenue',
      label: 'Revenue',
      render: v => <span className="text-emerald-400">{formatCurrency(v || 0)}</span>,
    },
    {
      key: 'ai_adoption_rate',
      label: 'AI Adoption',
      render: v => <span className="text-blue-400">{v?.toFixed(0)}%</span>,
    },
    {
      key: 'trend',
      label: 'Trend',
      render: v => v === 'up' ? (
        <span className="text-emerald-400 text-xs">Improving</span>
      ) : (
        <span className="text-red-400 text-xs">Declining</span>
      ),
    },
  ]

  if (loading) return <LoadingSpinner />

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Dealer Performance</h1>
        <select
          value={regionFilter}
          onChange={e => setRegionFilter(e.target.value)}
          className="bg-gray-800 text-white text-sm rounded-lg px-3 py-2 border border-gray-700 outline-none"
        >
          <option value="">All Regions</option>
          {[{ id: 1, name: 'North' }, { id: 2, name: 'South' }, { id: 3, name: 'East' }, { id: 4, name: 'West' }, { id: 5, name: 'Central' }].map(r => (
            <option key={r.id} value={r.id}>{r.name}</option>
          ))}
        </select>
      </div>

      <DataTable columns={columns} data={dealers} />
    </div>
  )
}
