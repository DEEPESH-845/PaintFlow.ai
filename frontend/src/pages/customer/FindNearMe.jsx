import { useState, useEffect } from 'react'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { fetchNearbyDealers } from '../../api/customer'
import { MapPinIcon } from '@heroicons/react/24/solid'

export default function FindNearMe() {
  const [dealers, setDealers] = useState([])
  const [loading, setLoading] = useState(true)
  const [lat, setLat] = useState(19.07)
  const [lng, setLng] = useState(72.87)

  useEffect(() => {
    setLoading(true)
    fetchNearbyDealers(lat, lng)
      .then(r => setDealers(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [lat, lng])

  const cities = [
    { name: 'Mumbai', lat: 19.07, lng: 72.87 },
    { name: 'Delhi', lat: 28.61, lng: 77.23 },
    { name: 'Chennai', lat: 13.08, lng: 80.27 },
    { name: 'Kolkata', lat: 22.57, lng: 88.36 },
    { name: 'Pune', lat: 18.52, lng: 73.85 },
    { name: 'Bangalore', lat: 12.97, lng: 77.59 },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Find Dealers Near You</h1>
        <p className="text-gray-500 mt-1">Locate authorized paint dealers in your area</p>
      </div>

      {/* Quick city selector */}
      <div className="flex flex-wrap gap-2">
        {cities.map(c => (
          <button
            key={c.name}
            onClick={() => { setLat(c.lat); setLng(c.lng) }}
            className={`px-4 py-2 rounded-lg text-sm transition-colors ${
              lat === c.lat && lng === c.lng
                ? 'bg-orange-500 text-white'
                : 'bg-white border border-gray-200 text-gray-600 hover:bg-gray-50'
            }`}
          >
            {c.name}
          </button>
        ))}
      </div>

      {loading ? (
        <LoadingSpinner text="Finding dealers..." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {dealers.map(d => (
            <div key={d.id} className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-gray-900">{d.name}</h3>
                  <p className="text-sm text-gray-500">{d.city}</p>
                </div>
                <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                  d.tier === 'Platinum' ? 'bg-purple-100 text-purple-700' :
                  d.tier === 'Gold' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-gray-100 text-gray-600'
                }`}>
                  {d.tier}
                </span>
              </div>
              <div className="mt-3 flex items-center gap-2 text-sm text-gray-500">
                <MapPinIcon className="w-4 h-4 text-orange-500" />
                {d.distance_km} km away
              </div>
            </div>
          ))}
          {dealers.length === 0 && (
            <p className="text-gray-400 col-span-2 text-center py-8">No dealers found within 50km</p>
          )}
        </div>
      )}
    </div>
  )
}
