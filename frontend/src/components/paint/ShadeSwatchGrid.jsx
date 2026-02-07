import { Link } from 'react-router-dom'
import { FireIcon } from '@heroicons/react/24/solid'

export default function ShadeSwatchGrid({ shades = [] }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {shades.map(shade => (
        <Link
          key={shade.id}
          to={`/customer/shade/${shade.id}`}
          className="group rounded-xl overflow-hidden bg-white shadow-sm hover:shadow-lg transition-all hover:-translate-y-1 border border-gray-100"
        >
          <div
            className="h-28 w-full"
            style={{ backgroundColor: shade.hex_color }}
          />
          <div className="p-3">
            <div className="flex items-center gap-1">
              <p className="font-medium text-gray-800 text-sm truncate">{shade.shade_name}</p>
              {shade.is_trending && <FireIcon className="w-3.5 h-3.5 text-orange-500 flex-shrink-0" />}
            </div>
            <p className="text-xs text-gray-500">{shade.shade_code}</p>
            <p className="text-[10px] text-gray-400 mt-1">{shade.product_name}</p>
          </div>
        </Link>
      ))}
    </div>
  )
}
