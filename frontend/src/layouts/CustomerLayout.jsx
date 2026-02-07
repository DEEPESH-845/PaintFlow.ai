import { NavLink, Outlet } from 'react-router-dom'
import {
  SwatchIcon, MapPinIcon, CameraIcon,
} from '@heroicons/react/24/outline'

const nav = [
  { to: '/customer', icon: SwatchIcon, label: 'Shade Catalog', end: true },
  { to: '/customer/find-near-me', icon: MapPinIcon, label: 'Find Near Me' },
  { to: '/customer/snap-find', icon: CameraIcon, label: 'Snap & Find' },
]

export default function CustomerLayout() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 to-white">
      {/* Top header */}
      <header className="bg-gradient-to-r from-orange-600 to-amber-500 text-white px-6 py-4 shadow-lg">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <NavLink to="/" className="text-xl font-bold">
            Paint<span className="text-yellow-200">Flow</span>.ai
          </NavLink>
          <nav className="flex gap-1">
            {nav.map(({ to, icon: Icon, label, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  `flex items-center gap-2 px-4 py-2 rounded-lg text-sm transition-colors ${
                    isActive ? 'bg-white/20 text-white' : 'text-white/70 hover:bg-white/10 hover:text-white'
                  }`
                }
              >
                <Icon className="w-4 h-4" />
                {label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-6xl mx-auto p-6">
        <Outlet />
      </main>
    </div>
  )
}
