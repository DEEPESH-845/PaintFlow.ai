import { Link } from 'react-router-dom'

const roles = [
  {
    title: 'Manufacturer Admin',
    desc: 'Global inventory visibility, demand forecasting, and supply chain orchestration.',
    path: '/admin',
    icon: '🏭',
    gradient: 'from-blue-900 to-blue-700',
    border: 'border-blue-500',
  },
  {
    title: 'Dealer Portal',
    desc: 'AI-powered ordering, inventory health monitoring, and smart restocking.',
    path: '/dealer',
    icon: '🏪',
    gradient: 'from-emerald-800 to-emerald-600',
    border: 'border-emerald-500',
  },
  {
    title: 'Customer',
    desc: 'Browse shades, check availability, and find paint near you.',
    path: '/customer',
    icon: '🎨',
    gradient: 'from-orange-700 to-amber-500',
    border: 'border-orange-400',
  },
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-8">
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold text-white mb-3">
          Paint<span className="text-emerald-400">Flow</span>.ai
        </h1>
        <p className="text-gray-400 text-lg">AI-Powered Supply Chain Intelligence for Paint Manufacturing</p>
        <p className="text-gray-600 text-sm mt-2">System Date: October 10, 2025</p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 max-w-5xl w-full">
        {roles.map((role) => (
          <Link
            key={role.path}
            to={role.path}
            className={`group relative bg-gradient-to-br ${role.gradient} rounded-2xl p-8 border ${role.border} border-opacity-30 hover:border-opacity-100 transition-all duration-300 hover:scale-105 hover:shadow-2xl`}
          >
            <div className="text-5xl mb-4">{role.icon}</div>
            <h2 className="text-2xl font-bold text-white mb-3">{role.title}</h2>
            <p className="text-gray-200 text-sm leading-relaxed">{role.desc}</p>
            <div className="mt-6 text-white/70 group-hover:text-white transition-colors text-sm">
              Enter →
            </div>
          </Link>
        ))}
      </div>

      <p className="text-gray-700 text-xs mt-12">
        Transforming reactive supply chains into self-healing intelligence networks.
      </p>
    </div>
  )
}
