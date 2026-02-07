import { useState, useEffect } from 'react'
import confetti from 'canvas-confetti'
import AlertBadge from '../../components/common/AlertBadge'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { fetchSmartOrders, acceptBundle } from '../../api/dealer'
import { formatCurrency, formatDate } from '../../utils/formatters'

const DEALER_ID = 1

export default function SmartOrders() {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [bundleResult, setBundleResult] = useState(null)

  useEffect(() => {
    fetchSmartOrders(DEALER_ID)
      .then(r => setOrders(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const totalSavings = orders.reduce((s, o) => s + (o.savings_amount || 0), 0)

  const handleAcceptBundle = async () => {
    try {
      const res = await acceptBundle(DEALER_ID)
      setBundleResult(res.data)
      confetti({
        particleCount: 150,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#10b981', '#3b82f6', '#f59e0b'],
      })
    } catch {
      setBundleResult({ message: 'Failed to accept bundle' })
    }
  }

  if (loading) return <LoadingSpinner />

  if (bundleResult) {
    return (
      <div className="flex flex-col items-center justify-center py-20">
        <div className="glass rounded-2xl p-10 border border-emerald-500/30 text-center max-w-md">
          <div className="text-5xl mb-4">🎉</div>
          <h2 className="text-2xl font-bold text-white mb-2">Bundle Accepted!</h2>
          <p className="text-emerald-400 text-lg font-semibold mb-2">
            You saved {formatCurrency(bundleResult.total_savings || 0)}
          </p>
          <p className="text-gray-400 text-sm">{bundleResult.message}</p>
          <p className="text-gray-500 text-xs mt-4">{bundleResult.orders_placed} orders placed</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Smart Restock</h1>
          <p className="text-sm text-gray-500 mt-1">AI-powered order recommendations</p>
        </div>
      </div>

      {/* Accept All CTA */}
      {orders.length > 0 && (
        <button
          onClick={handleAcceptBundle}
          className="w-full glow-btn py-4 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 text-white rounded-xl text-lg font-bold transition-all flex items-center justify-center gap-3"
        >
          Accept All AI Recommendations
          <span className="bg-white/20 px-3 py-1 rounded-lg text-sm">
            Save {formatCurrency(totalSavings)}
          </span>
        </button>
      )}

      {/* Order Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {orders.map(order => (
          <div key={order.sku_id} className="glass rounded-xl p-5 border border-gray-800 hover:border-gray-700 transition-colors">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg" style={{ backgroundColor: order.shade_hex }} />
                <div>
                  <p className="text-white font-semibold">{order.shade_name}</p>
                  <p className="text-xs text-gray-500">{order.sku_code} | {order.size}</p>
                </div>
              </div>
              <AlertBadge status={order.urgency} />
            </div>

            <p className="text-xs text-gray-400 mb-3">{order.reason}</p>

            <div className="grid grid-cols-3 gap-2 text-xs mb-3">
              <div>
                <span className="text-gray-500">Current Stock</span>
                <p className="text-white font-mono">{order.current_stock}</p>
              </div>
              <div>
                <span className="text-gray-500">Recommended</span>
                <p className="text-white font-mono">{order.recommended_qty}</p>
              </div>
              <div>
                <span className="text-gray-500">Stockout Date</span>
                <p className="text-red-400 font-mono">{formatDate(order.predicted_stockout_date)}</p>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-500">
                Total: {formatCurrency(order.total_cost || 0)}
              </span>
              <span className="bg-emerald-500/20 text-emerald-400 px-2 py-1 rounded text-xs font-semibold">
                Save {formatCurrency(order.savings_amount || 0)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
