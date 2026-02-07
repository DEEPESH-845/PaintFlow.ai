export default function HealthScoreGauge({ score = 0 }) {
  const radius = 60
  const circumference = 2 * Math.PI * radius
  const pct = Math.min(100, Math.max(0, score)) / 100
  const offset = circumference - pct * circumference

  const getColor = (s) => {
    if (s >= 70) return '#10b981'
    if (s >= 40) return '#f59e0b'
    return '#ef4444'
  }
  const color = getColor(score)

  return (
    <div className="flex flex-col items-center">
      <svg width="150" height="150" viewBox="0 0 150 150">
        <circle
          cx="75" cy="75" r={radius}
          fill="none" stroke="#1f2937" strokeWidth="10"
        />
        <circle
          cx="75" cy="75" r={radius}
          fill="none" stroke={color} strokeWidth="10"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform="rotate(-90 75 75)"
          style={{ transition: 'stroke-dashoffset 1s ease' }}
        />
        <text x="75" y="70" textAnchor="middle" fill="white" fontSize="28" fontWeight="bold">
          {Math.round(score)}
        </text>
        <text x="75" y="90" textAnchor="middle" fill="#6b7280" fontSize="11">
          Health Score
        </text>
      </svg>
    </div>
  )
}
