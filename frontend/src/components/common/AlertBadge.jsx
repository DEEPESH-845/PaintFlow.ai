const styles = {
  critical: 'bg-red-500/20 text-red-400 border-red-500/30',
  low: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  healthy: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  overstocked: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  CRITICAL: 'bg-red-500/20 text-red-400 border-red-500/30',
  RECOMMENDED: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  OPTIONAL: 'bg-gray-500/20 text-gray-400 border-gray-500/30',
  PENDING: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  APPROVED: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
  IN_TRANSIT: 'bg-cyan-500/20 text-cyan-400 border-cyan-500/30',
  COMPLETED: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
}

export default function AlertBadge({ status }) {
  return (
    <span className={`inline-flex px-2 py-0.5 rounded-full text-[10px] font-semibold uppercase tracking-wider border ${styles[status] || styles.healthy}`}>
      {status?.replace('_', ' ')}
    </span>
  )
}
