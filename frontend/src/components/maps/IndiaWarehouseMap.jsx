import { useState } from 'react'
import { ComposableMap, Geographies, Geography, Marker, Line } from 'react-simple-maps'

const GEO_URL = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json'

const statusConfig = {
  critical: { color: '#ef4444', pulse: 'marker-critical', label: 'Critical' },
  low: { color: '#f59e0b', pulse: 'marker-low', label: 'Low' },
  healthy: { color: '#10b981', pulse: 'marker-healthy', label: 'Healthy' },
  overstocked: { color: '#3b82f6', pulse: 'marker-overstocked', label: 'Overstocked' },
}

export default function IndiaWarehouseMap({ warehouses = [], transfers = [], onSelectWarehouse }) {
  const [tooltip, setTooltip] = useState(null)

  const activeTransfers = transfers.filter(t => t.status === 'IN_TRANSIT' || t.status === 'APPROVED')

  return (
    <div className="relative bg-gray-900/50 rounded-xl border border-gray-800 overflow-hidden">
      {/* Legend */}
      <div className="absolute top-3 right-3 z-10 glass rounded-lg p-3 space-y-1.5">
        {Object.entries(statusConfig).map(([key, { color, label }]) => (
          <div key={key} className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full" style={{ background: color }} />
            <span className="text-[10px] text-gray-400">{label}</span>
          </div>
        ))}
      </div>

      <ComposableMap
        projection="geoMercator"
        projectionConfig={{ center: [82, 22], scale: 1000 }}
        width={500}
        height={500}
        style={{ width: '100%', height: 'auto' }}
      >
        <Geographies geography={GEO_URL}>
          {({ geographies }) =>
            geographies
              .filter(g => g.properties.name === 'India')
              .map(geo => (
                <Geography
                  key={geo.rpiKey || geo.id}
                  geography={geo}
                  fill="#1e293b"
                  stroke="#334155"
                  strokeWidth={0.5}
                />
              ))
          }
        </Geographies>

        {/* Transfer arcs */}
        {activeTransfers.map((t, i) => (
          t.from_warehouse && t.to_warehouse && (
            <Line
              key={i}
              from={[t.from_warehouse.lng, t.from_warehouse.lat]}
              to={[t.to_warehouse.lng, t.to_warehouse.lat]}
              stroke="#f59e0b"
              strokeWidth={2}
              className="transfer-arc"
              strokeLinecap="round"
            />
          )
        ))}

        {/* Warehouse markers */}
        {warehouses.map(wh => {
          const cfg = statusConfig[wh.status] || statusConfig.healthy
          return (
            <Marker
              key={wh.id}
              coordinates={[wh.longitude, wh.latitude]}
              onClick={() => onSelectWarehouse?.(wh)}
              onMouseEnter={() => setTooltip(wh)}
              onMouseLeave={() => setTooltip(null)}
            >
              <circle
                r={6}
                fill={cfg.color}
                className={cfg.pulse}
                style={{ cursor: 'pointer' }}
              />
              <text
                textAnchor="middle"
                y={-12}
                style={{ fill: '#9ca3af', fontSize: 8, fontWeight: 600 }}
              >
                {wh.city}
              </text>
            </Marker>
          )
        })}
      </ComposableMap>

      {/* Tooltip */}
      {tooltip && (
        <div className="absolute bottom-4 left-4 glass rounded-lg p-3 min-w-[200px] z-20">
          <p className="font-semibold text-white text-sm">{tooltip.name}</p>
          <p className="text-xs text-gray-400">{tooltip.city}, {tooltip.state}</p>
          <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
            <div>
              <span className="text-gray-500">Capacity</span>
              <p className="text-white">{tooltip.capacity_pct}%</p>
            </div>
            <div>
              <span className="text-gray-500">Stock</span>
              <p className="text-white">{tooltip.total_stock?.toLocaleString('en-IN')}</p>
            </div>
            {tooltip.critical_skus > 0 && (
              <div>
                <span className="text-red-400">Critical SKUs</span>
                <p className="text-red-400 font-bold">{tooltip.critical_skus}</p>
              </div>
            )}
            {tooltip.revenue_at_risk > 0 && (
              <div>
                <span className="text-red-400">Revenue at Risk</span>
                <p className="text-red-400 font-bold">{`\u20B9${(tooltip.revenue_at_risk / 1000).toFixed(0)}K`}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
