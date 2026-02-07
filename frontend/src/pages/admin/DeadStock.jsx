import { useState, useEffect } from 'react'
import DataTable from '../../components/common/DataTable'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import AlertBadge from '../../components/common/AlertBadge'
import { fetchDeadStock } from '../../api/admin'
import { formatCurrency } from '../../utils/formatters'

export default function DeadStock() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDeadStock()
      .then(r => setData(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />

  const totalCapitalLocked = data.reduce((s, d) => s + (d.capital_locked || 0), 0)

  const columns = [
    {
      key: 'shade_name',
      label: 'Shade',
      render: (v, row) => (
        <div className="flex items-center gap-2">
          <span className="w-4 h-4 rounded" style={{ backgroundColor: row.shade_hex }} />
          <span className="text-white font-medium">{v}</span>
        </div>
      ),
    },
    { key: 'sku_code', label: 'SKU' },
    { key: 'size', label: 'Size' },
    { key: 'warehouse', label: 'Warehouse', render: (v, row) => `${v} (${row.warehouse_city})` },
    { key: 'current_stock', label: 'Stock', render: v => v?.toLocaleString('en-IN') },
    {
      key: 'days_of_cover',
      label: 'Days Cover',
      render: v => <span className="text-blue-400 font-mono">{v?.toFixed(0)}d</span>,
    },
    {
      key: 'capital_locked',
      label: 'Capital Locked',
      render: v => <span className="text-yellow-400">{formatCurrency(v || 0)}</span>,
    },
    {
      key: 'recommendation',
      label: 'Action',
      render: v => (
        <span className="text-xs text-gray-400">{v}</span>
      ),
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Dead Stock Analysis</h1>
          <p className="text-sm text-gray-500 mt-1">SKUs with &gt;90 days of inventory cover</p>
        </div>
        <div className="glass rounded-xl px-4 py-3 border border-yellow-500/30">
          <p className="text-xs text-gray-500">Total Capital Locked</p>
          <p className="text-xl font-bold text-yellow-400">{formatCurrency(totalCapitalLocked)}</p>
        </div>
      </div>

      <DataTable columns={columns} data={data} />
    </div>
  )
}
