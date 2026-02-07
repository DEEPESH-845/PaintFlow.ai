import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { formatCurrency } from '../../utils/formatters'

export default function InventoryBarChart({ data = [] }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
        <XAxis
          dataKey="shade_name"
          tick={{ fill: '#9ca3af', fontSize: 10 }}
          angle={-30}
          textAnchor="end"
          height={60}
        />
        <YAxis tick={{ fill: '#9ca3af', fontSize: 11 }} tickFormatter={v => formatCurrency(v)} />
        <Tooltip
          contentStyle={{ background: '#111827', border: '1px solid #374151', borderRadius: 8 }}
          formatter={(v) => [formatCurrency(v), 'Revenue']}
        />
        <Bar dataKey="total_revenue" radius={[4, 4, 0, 0]}>
          {data.map((entry, i) => (
            <Cell key={i} fill={entry.shade_hex || '#3b82f6'} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
