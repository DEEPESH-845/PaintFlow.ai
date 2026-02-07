import { useState, useEffect } from 'react'
import {
  CubeIcon, BuildingOffice2Icon, UserGroupIcon,
  CurrencyRupeeIcon, ExclamationTriangleIcon, ArrowsRightLeftIcon,
  ArchiveBoxXMarkIcon, BanknotesIcon,
} from '@heroicons/react/24/outline'
import StatCard from '../../components/common/StatCard'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import IndiaWarehouseMap from '../../components/maps/IndiaWarehouseMap'
import InventoryBarChart from '../../components/charts/InventoryBarChart'
import AICopilotChat from '../../components/copilot/AICopilotChat'
import { fetchDashboardSummary, fetchInventoryMap, fetchTransfers, fetchTopSkus } from '../../api/admin'
import { useSimulation } from '../../contexts/SimulationContext'
import { formatCurrency } from '../../utils/formatters'

export default function AdminDashboard() {
  const [summary, setSummary] = useState(null)
  const [warehouses, setWarehouses] = useState([])
  const [transfers, setTransfers] = useState([])
  const [topSkus, setTopSkus] = useState([])
  const [loading, setLoading] = useState(true)
  const { scenario, currentData } = useSimulation()

  useEffect(() => {
    setLoading(true)
    Promise.all([
      fetchDashboardSummary(),
      fetchInventoryMap(),
      fetchTransfers(),
      fetchTopSkus(),
    ]).then(([s, m, t, ts]) => {
      setSummary(s.data)
      setWarehouses(m.data)
      setTransfers(t.data)
      setTopSkus(ts.data)
    }).catch(() => {}).finally(() => setLoading(false))
  }, [])

  if (loading) return <LoadingSpinner text="Loading dashboard..." />

  // Override with scenario data when simulation active
  const dash = scenario !== 'NORMAL' && currentData?.dashboard_summary
    ? { ...summary, ...currentData.dashboard_summary }
    : summary

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Command Center</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard
          title="Revenue (MTD)"
          value={formatCurrency(dash?.total_revenue_mtd || 0)}
          icon={CurrencyRupeeIcon}
          color="green"
          trend="up"
        />
        <StatCard
          title="Stockout Alerts"
          value={dash?.stockout_count || 0}
          icon={ExclamationTriangleIcon}
          color="red"
          subtitle="SKUs below 3-day cover"
        />
        <StatCard
          title="Revenue at Risk"
          value={formatCurrency(dash?.revenue_at_risk || 0)}
          icon={BanknotesIcon}
          color="red"
        />
        <StatCard
          title="Pending Transfers"
          value={dash?.pending_transfers || 0}
          icon={ArrowsRightLeftIcon}
          color="yellow"
        />
        <StatCard
          title="Total SKUs"
          value={dash?.total_skus || 0}
          icon={CubeIcon}
          color="blue"
        />
        <StatCard
          title="Warehouses"
          value={dash?.total_warehouses || 0}
          icon={BuildingOffice2Icon}
          color="cyan"
        />
        <StatCard
          title="Active Dealers"
          value={dash?.total_dealers || 0}
          icon={UserGroupIcon}
          color="purple"
        />
        <StatCard
          title="Dead Stock"
          value={dash?.dead_stock_count || 0}
          icon={ArchiveBoxXMarkIcon}
          color="yellow"
          subtitle=">90 days cover"
        />
      </div>

      {/* Map + Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h2 className="text-sm font-medium text-gray-400 mb-3">Warehouse Network</h2>
          <IndiaWarehouseMap warehouses={warehouses} transfers={transfers} />
        </div>
        <div>
          <h2 className="text-sm font-medium text-gray-400 mb-3">Top SKUs by Revenue</h2>
          <div className="glass rounded-xl p-4 border border-gray-800">
            <InventoryBarChart data={topSkus} />
          </div>
        </div>
      </div>

      <AICopilotChat />
    </div>
  )
}
