import { NavLink, Outlet } from 'react-router-dom'
import {
  HomeIcon, SparklesIcon, ClipboardDocumentListIcon,
} from '@heroicons/react/24/outline'

const nav = [
  { to: '/dealer', icon: HomeIcon, label: 'Dashboard', end: true },
  { to: '/dealer/smart-orders', icon: SparklesIcon, label: 'Smart Orders' },
  { to: '/dealer/orders', icon: ClipboardDocumentListIcon, label: 'Order History' },
]

export default function DealerLayout() {
  return (
    <div className="flex h-screen bg-gray-950 text-white">
      <aside className="w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
        <div className="p-6 border-b border-gray-800">
          <NavLink to="/" className="text-xl font-bold">
            Paint<span className="text-emerald-400">Flow</span>.ai
          </NavLink>
          <p className="text-xs text-emerald-500 mt-1">Dealer Portal</p>
        </div>
        <nav className="flex-1 p-4 space-y-1">
          {nav.map(({ to, icon: Icon, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm transition-colors ${
                  isActive ? 'bg-emerald-600/20 text-emerald-400' : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="p-4 border-t border-gray-800 text-xs text-gray-600">
          Dealer ID: D-001 | Mumbai
        </div>
      </aside>

      <main className="flex-1 overflow-auto p-6">
        <Outlet />
      </main>
    </div>
  )
}
