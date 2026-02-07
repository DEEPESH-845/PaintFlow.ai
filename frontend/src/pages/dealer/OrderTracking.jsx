import { useState, useEffect } from 'react'
import DataTable from '../../components/common/DataTable'
import AlertBadge from '../../components/common/AlertBadge'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { fetchOrders } from '../../api/dealer'
import { formatCurrency, formatDate } from '../../utils/formatters'

const DEALER_ID = 1

export default function OrderTracking() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchOrders(DEALER_ID)
      .then(r => setOrders(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />

  const columns = [
    { key: 'id', label: 'Order ID', render: v => <span className="font-mono text-gray-400">#{v}</span> },
    { key: 'sku_id', label: 'SKU ID' },
    { key: 'quantity', label: 'Qty', render: v => v?.toLocaleString('en-IN') },
    {
      key: 'order_date',
      label: 'Date',
      render: v => v ? formatDate(v) : '-',
    },
    {
      key: 'status',
      label: 'Status',
      render: v => <AlertBadge status={v?.toUpperCase()} />,
    },
    {
      key: 'is_ai_suggested',
      label: 'Source',
      render: v => v ? (
        <span className="text-xs text-blue-400">AI Recommended</span>
      ) : (
        <span className="text-xs text-gray-500">Manual</span>
      ),
    },
    {
      key: 'savings_amount',
      label: 'Savings',
      render: v => v > 0 ? (
        <span className="text-emerald-400 text-xs">{formatCurrency(v)}</span>
      ) : (
        <span className="text-gray-600">-</span>
      ),
    },
  ]

  const totalSavings = orders.reduce((s, o) => s + (o.savings_amount || 0), 0)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Order History</h1>
          <p className="text-sm text-gray-500 mt-1">Last 50 orders</p>
        </div>
        {totalSavings > 0 && (
          <div className="glass rounded-xl px-4 py-3 border border-emerald-500/30">
            <p className="text-xs text-gray-500">Total AI Savings</p>
            <p className="text-xl font-bold text-emerald-400">{formatCurrency(totalSavings)}</p>
          </div>
        )}
      </div>

      <DataTable columns={columns} data={orders} />
    </div>
  )
}
