import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { fetchShadeDetail, fetchShadeAvailability } from '../../api/customer'
import { FireIcon, MapPinIcon } from '@heroicons/react/24/solid'

export default function ShadeDetail() {
  const { shadeId } = useParams()
  const [shade, setShade] = useState(null)
  const [availability, setAvailability] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetchShadeDetail(shadeId),
      fetchShadeAvailability(shadeId, 19.07, 72.87),
    ]).then(([s, a]) => {
      setShade(s.data)
      setAvailability(a.data)
    }).catch(() => {}).finally(() => setLoading(false))
  }, [shadeId])

  if (loading) return <LoadingSpinner />
  if (!shade) return <p className="text-gray-500">Shade not found</p>

  return (
    <div className="space-y-6">
      <Link to="/customer" className="text-orange-500 hover:text-orange-600 text-sm">&larr; Back to catalog</Link>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Color preview */}
        <div>
          <div
            className="h-64 rounded-2xl shadow-xl"
            style={{ backgroundColor: shade.hex_color }}
          />
          <div className="mt-4 flex items-center gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{shade.shade_name}</h1>
              <p className="text-gray-500">{shade.shade_code} | {shade.shade_family}</p>
            </div>
            {shade.is_trending && (
              <span className="flex items-center gap-1 bg-orange-100 text-orange-600 px-3 py-1 rounded-full text-xs font-medium">
                <FireIcon className="w-3.5 h-3.5" /> Trending
              </span>
            )}
          </div>

          <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-gray-500">HEX</span>
              <p className="font-mono text-gray-900">{shade.hex_color}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-gray-500">RGB</span>
              <p className="font-mono text-gray-900">
                {shade.rgb?.r}, {shade.rgb?.g}, {shade.rgb?.b}
              </p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-gray-500">Product</span>
              <p className="text-gray-900">{shade.product?.name}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-gray-500">Finish</span>
              <p className="text-gray-900">{shade.product?.finish}</p>
            </div>
          </div>
        </div>

        {/* Sizes + availability */}
        <div className="space-y-6">
          <div>
            <h3 className="font-semibold text-gray-900 mb-3">Available Sizes</h3>
            <div className="grid grid-cols-2 gap-3">
              {shade.sizes?.map(s => (
                <div key={s.sku_code} className="bg-white border border-gray-200 rounded-xl p-4 hover:shadow-md transition-shadow">
                  <p className="font-bold text-gray-900">{s.size}</p>
                  <p className="text-xs text-gray-500">{s.sku_code}</p>
                  <p className="text-lg font-bold text-orange-600 mt-1">{`\u20B9${s.mrp?.toLocaleString('en-IN')}`}</p>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <MapPinIcon className="w-4 h-4 text-orange-500" />
              Nearby Dealers
            </h3>
            {availability.length === 0 ? (
              <p className="text-sm text-gray-400">No nearby dealers found</p>
            ) : (
              <div className="space-y-2">
                {availability.map(d => (
                  <div key={d.dealer_id} className="bg-white border border-gray-200 rounded-xl p-3 flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900 text-sm">{d.dealer_name}</p>
                      <p className="text-xs text-gray-500">{d.city} | {d.distance_km} km away</p>
                    </div>
                    <span className={`text-xs font-semibold px-2 py-1 rounded-full ${
                      d.stock_status === 'In Stock' ? 'bg-emerald-100 text-emerald-700' :
                      d.stock_status === 'Low Stock' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {d.stock_status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
