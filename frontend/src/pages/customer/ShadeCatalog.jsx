import { useState, useEffect } from 'react'
import ShadeSwatchGrid from '../../components/paint/ShadeSwatchGrid'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { fetchShades } from '../../api/customer'

const families = ['All', 'Reds', 'Blues', 'Greens', 'Yellows', 'Neutrals', 'Whites']
const categories = ['All', 'Interior Wall', 'Exterior Wall', 'Wood & Metal', 'Waterproofing']

export default function ShadeCatalog() {
  const [shades, setShades] = useState([])
  const [loading, setLoading] = useState(true)
  const [family, setFamily] = useState('All')
  const [category, setCategory] = useState('All')
  const [trending, setTrending] = useState(false)

  useEffect(() => {
    setLoading(true)
    const params = {}
    if (family !== 'All') params.family = family
    if (category !== 'All') params.category = category
    if (trending) params.trending = true

    fetchShades(params)
      .then(r => setShades(r.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [family, category, trending])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Explore Shades</h1>
        <p className="text-gray-500 mt-1">Find the perfect color for your home</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 items-center">
        <div className="flex gap-1">
          {families.map(f => (
            <button
              key={f}
              onClick={() => setFamily(f)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                family === f
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {f}
            </button>
          ))}
        </div>

        <select
          value={category}
          onChange={e => setCategory(e.target.value)}
          className="bg-white border border-gray-200 text-gray-700 text-sm rounded-lg px-3 py-1.5 outline-none"
        >
          {categories.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>

        <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
          <input
            type="checkbox"
            checked={trending}
            onChange={e => setTrending(e.target.checked)}
            className="rounded border-gray-300"
          />
          Trending Only
        </label>
      </div>

      {loading ? (
        <LoadingSpinner text="Loading shades..." />
      ) : (
        <>
          <p className="text-sm text-gray-400">{shades.length} shades found</p>
          <ShadeSwatchGrid shades={shades} />
        </>
      )}
    </div>
  )
}
