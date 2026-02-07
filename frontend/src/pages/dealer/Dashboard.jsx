import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  ShoppingCartIcon, CurrencyRupeeIcon,
  SparklesIcon, ExclamationTriangleIcon,
} from '@heroicons/react/24/outline'
import StatCard from '../../components/common/StatCard'
import HealthScoreGauge from '../../components/paint/HealthScoreGauge'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { fetchDealerDashboard, fetchDealerAlerts } from '../../api/dealer'
import { formatCurrency } from '../../utils/formatters'

const DEALER_ID = 1

export default function DealerDashboard() {
  const [data, setData] = useState(null)
  const [alerts, setAlerts] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetchDealerDashboard(DEALER_ID),
      fetchDealerAlerts(DEALER_ID),
    ]).then(([d, a]) => {
      setData(d.data)
      setAlerts(a.data)
    }).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner />
  if (!data) return <p className="text-gray-500">Dealer not found</p>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">{data.dealer?.name}</h1>
          <p className="text-sm text-gray-500">{data.dealer?.city} | Tier: {data.dealer?.tier}</p>
        </div>
        <Link
          to="/dealer/smart-orders"
          className="glow-btn px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-sm font-medium flex items-center gap-2 transition-all"
        >
          <SparklesIcon className="w-4 h-4" />
          View Smart Orders
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Health Score */}
        <div className="glass rounded-xl p-6 border border-gray-800 flex items-center justify-center">
          <HealthScoreGauge score={data.health_score || 0} />
        </div>

        {/* KPIs */}
        <div className="col-span-2 grid grid-cols-2 gap-4">
          <StatCard
            title="Total Orders"
            value={data.total_orders || 0}
            icon={ShoppingCartIcon}
            color="blue"
          />
          <StatCard
            title="Revenue (MTD)"
            value={formatCurrency(data.revenue_this_month || 0)}
            icon={CurrencyRupeeIcon}
            color="green"
          />
          <StatCard
            title="AI Recommendations"
            value={data.ai_recommendations_pending || 0}
            icon={SparklesIcon}
            color="purple"
            subtitle="Pending action"
          />
          <StatCard
            title="AI Savings"
            value={formatCurrency(data.total_ai_savings || 0)}
            icon={CurrencyRupeeIcon}
            color="cyan"
            subtitle="Total saved with AI"
          />
        </div>
      </div>

      {/* Alerts */}
      {alerts && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Stockout alerts */}
          <div className="glass rounded-xl p-5 border border-red-500/20">
            <h3 className="text-sm font-medium text-red-400 mb-3 flex items-center gap-2">
              <ExclamationTriangleIcon className="w-4 h-4" />
              Stockout Alerts
            </h3>
            {alerts.stockout_alerts?.length === 0 && (
              <p className="text-xs text-gray-600">No critical stockouts</p>
            )}
            <div className="space-y-2">
              {alerts.stockout_alerts?.map((a, i) => (
                <div key={i} className="flex items-center justify-between text-sm">
                  <div className="flex items-center gap-2">
                    <span className="w-3 h-3 rounded" style={{ backgroundColor: a.shade_hex }} />
                    <span className="text-white">{a.shade_name}</span>
                  </div>
                  <span className="text-red-400 text-xs font-mono">{a.days_remaining?.toFixed(1)}d left</span>
                </div>
              ))}
            </div>
          </div>

          {/* Trending */}
          <div className="glass rounded-xl p-5 border border-orange-500/20">
            <h3 className="text-sm font-medium text-orange-400 mb-3">Trending Shades</h3>
            <div className="space-y-2">
              {alerts.trending?.map((t, i) => (
                <div key={i} className="flex items-center gap-2 text-sm">
                  <span className="w-3 h-3 rounded" style={{ backgroundColor: t.shade_hex }} />
                  <span className="text-white">{t.shade_name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
