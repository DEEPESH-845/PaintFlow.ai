import { useState, useEffect, useCallback } from 'react'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import AlertBadge from '../../components/common/AlertBadge'
import IndiaWarehouseMap from '../../components/maps/IndiaWarehouseMap'
import { fetchTransfers, approveTransfer, fetchInventoryMap } from '../../api/admin'

export default function Transfers() {
  const [transfers, setTransfers] = useState([])
  const [warehouses, setWarehouses] = useState([])
  const [loading, setLoading] = useState(true)
  const [toast, setToast] = useState(null)

  const load = useCallback(() => {
    Promise.all([fetchTransfers(), fetchInventoryMap()])
      .then(([t, w]) => {
        setTransfers(t.data)
        setWarehouses(w.data)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => { load() }, [load])

  const handleApprove = async (id) => {
    try {
      const res = await approveTransfer(id)
      setToast(res.data.message)
      load() // Refresh data (optimistic update from backend)
      setTimeout(() => setToast(null), 5000)
    } catch {
      setToast('Failed to approve transfer')
      setTimeout(() => setToast(null), 3000)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Transfer Management</h1>

      {/* Toast */}
      {toast && (
        <div className="fixed top-4 right-4 z-50 bg-emerald-600 text-white px-6 py-3 rounded-xl shadow-2xl text-sm animate-bounce">
          {toast}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Map */}
        <div>
          <h2 className="text-sm font-medium text-gray-400 mb-3">Transfer Network</h2>
          <IndiaWarehouseMap warehouses={warehouses} transfers={transfers} />
        </div>

        {/* Transfer list */}
        <div className="space-y-3">
          <h2 className="text-sm font-medium text-gray-400 mb-3">
            Recommended Transfers ({transfers.length})
          </h2>
          {transfers.map(t => (
            <div key={t.id} className="glass rounded-xl p-4 border border-gray-800">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="w-4 h-4 rounded" style={{ backgroundColor: t.shade_hex }} />
                  <span className="text-white font-medium text-sm">{t.shade_name}</span>
                  <span className="text-xs text-gray-500">{t.sku_code}</span>
                </div>
                <AlertBadge status={t.status} />
              </div>

              <div className="flex items-center gap-2 text-xs text-gray-400 mb-2">
                <span className="text-white">{t.from_warehouse?.city}</span>
                <span className="text-yellow-400">→</span>
                <span className="text-white">{t.to_warehouse?.city}</span>
                <span className="text-gray-600">|</span>
                <span>{t.quantity} units</span>
              </div>

              <p className="text-xs text-gray-500 mb-3">{t.reason}</p>

              {t.status === 'PENDING' && (
                <div className="flex gap-2">
                  <button
                    onClick={() => handleApprove(t.id)}
                    className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs rounded-lg transition-colors"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => handleApprove(t.id)}
                    className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs rounded-lg transition-colors"
                  >
                    Auto-Balance
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
