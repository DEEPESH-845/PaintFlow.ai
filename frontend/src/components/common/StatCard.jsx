import { ArrowTrendingUpIcon, ArrowTrendingDownIcon } from '@heroicons/react/24/solid'

export default function StatCard({ title, value, subtitle, trend, icon: Icon, color = 'blue' }) {
  const colors = {
    blue: 'from-blue-600/20 to-blue-900/20 border-blue-500/30',
    green: 'from-emerald-600/20 to-emerald-900/20 border-emerald-500/30',
    red: 'from-red-600/20 to-red-900/20 border-red-500/30',
    yellow: 'from-yellow-600/20 to-yellow-900/20 border-yellow-500/30',
    purple: 'from-purple-600/20 to-purple-900/20 border-purple-500/30',
    cyan: 'from-cyan-600/20 to-cyan-900/20 border-cyan-500/30',
  }

  return (
    <div className={`glass bg-gradient-to-br ${colors[color]} rounded-xl p-5 border transition-transform hover:scale-[1.02]`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs text-gray-400 uppercase tracking-wider">{title}</p>
          <p className="text-2xl font-bold text-white mt-1">{value}</p>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className="flex flex-col items-end gap-2">
          {Icon && <Icon className="w-6 h-6 text-gray-500" />}
          {trend && (
            <span className={`flex items-center gap-1 text-xs ${trend === 'up' ? 'text-emerald-400' : 'text-red-400'}`}>
              {trend === 'up' ? <ArrowTrendingUpIcon className="w-3 h-3" /> : <ArrowTrendingDownIcon className="w-3 h-3" />}
              {trend === 'up' ? '+8%' : '-3%'}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}
