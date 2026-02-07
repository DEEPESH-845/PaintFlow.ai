import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  Area, ComposedChart, ReferenceLine, ResponsiveContainer,
} from 'recharts'

export default function ForecastChart({ actual = [], forecast = [], annotations = [], shadeHex = '#3B82F6' }) {
  // Merge actual and forecast data
  const merged = []

  actual.forEach(d => {
    merged.push({ date: d.date, actual: d.actual, label: new Date(d.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }) })
  })

  forecast.forEach(d => {
    merged.push({
      date: d.date,
      predicted: d.predicted,
      upper: d.upper,
      lower: d.lower,
      label: new Date(d.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }),
    })
  })

  return (
    <ResponsiveContainer width="100%" height={350}>
      <ComposedChart data={merged} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
        <XAxis
          dataKey="label"
          tick={{ fill: '#6b7280', fontSize: 10 }}
          interval={Math.floor(merged.length / 10)}
        />
        <YAxis tick={{ fill: '#6b7280', fontSize: 11 }} />
        <Tooltip
          contentStyle={{ background: '#111827', border: '1px solid #374151', borderRadius: 8 }}
          labelStyle={{ color: '#9ca3af' }}
        />

        {/* Confidence band */}
        <Area type="monotone" dataKey="upper" stroke="none" fill={shadeHex} fillOpacity={0.08} />
        <Area type="monotone" dataKey="lower" stroke="none" fill={shadeHex} fillOpacity={0.08} />

        {/* Actual line */}
        <Line
          type="monotone" dataKey="actual" stroke={shadeHex}
          strokeWidth={2} dot={false} connectNulls={false}
        />

        {/* Forecast line */}
        <Line
          type="monotone" dataKey="predicted" stroke={shadeHex}
          strokeWidth={2} strokeDasharray="6 3" dot={false}
        />

        {/* Event annotations */}
        {annotations.map((a, i) => (
          <ReferenceLine
            key={i}
            x={new Date(a.date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}
            stroke={a.color}
            strokeDasharray="4 4"
            label={{ value: a.label, fill: a.color, fontSize: 10, position: 'top' }}
          />
        ))}
      </ComposedChart>
    </ResponsiveContainer>
  )
}
