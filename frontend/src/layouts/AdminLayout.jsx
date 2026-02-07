import { NavLink, Outlet } from 'react-router-dom'
import { useSimulation } from '../contexts/SimulationContext'
import {
  HomeIcon, ChartBarIcon, ArchiveBoxXMarkIcon,
  ArrowsRightLeftIcon, UserGroupIcon,
} from '@heroicons/react/24/outline'

const nav = [
  { to: '/admin', icon: HomeIcon, label: 'Dashboard', end: true },
  { to: '/admin/forecast', icon: ChartBarIcon, label: 'Demand Forecast' },
  { to: '/admin/dead-stock', icon: ArchiveBoxXMarkIcon, label: 'Dead Stock' },
  { to: '/admin/transfers', icon: ArrowsRightLeftIcon, label: 'Transfers' },
  { to: '/admin/dealers', icon: UserGroupIcon, label: 'Dealer Performance' },
]

const scenarioColors = {
  NORMAL: 'bg-gray-700',
  TRUCK_STRIKE: 'bg-red-600',
  HEATWAVE: 'bg-orange-600',
  EARLY_MONSOON: 'bg-cyan-600',
}

export default function AdminLayout() {
  const { scenario, setScenario } = useSimulation()

  return (
    <div className="flex h-screen bg-gray-950 text-white">
      {/* Sidebar */}
      <aside className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
        <div className="p-6 border-b border-gray-800">
          <NavLink to="/" className="text-xl font-bold">
            Paint<span className="text-blue-400">Flow</span>.ai
          </NavLink>
          <p className="text-xs text-gray-500 mt-1">Manufacturer Admin</p>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {nav.map(({ to, icon: Icon, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive ? 'bg-blue-600/20 text-blue-400' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-gray-800 text-xs text-gray-600">
          System Date: Oct 10, 2025
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Scenario toggle bar */}
        <header className="bg-gray-900/80 border-b border-gray-800 px-6 py-3 flex items-center gap-3">
          <span className="text-xs text-gray-500 mr-2">Simulate:</span>
          {['NORMAL', 'TRUCK_STRIKE', 'HEATWAVE', 'EARLY_MONSOON'].map(s => (
            <button
              key={s}
              onClick={() => setScenario(s)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                scenario === s
                  ? `${scenarioColors[s]} text-white shadow-lg`
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}
            >
              {s === 'NORMAL' ? 'Normal' : s === 'TRUCK_STRIKE' ? 'Truck Strike' : s === 'HEATWAVE' ? 'Heatwave' : 'Early Monsoon'}
            </button>
          ))}
          {scenario !== 'NORMAL' && (
            <span className="ml-auto text-xs text-yellow-400 animate-pulse">
              Simulation Active
            </span>
          )}
        </header>

        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
