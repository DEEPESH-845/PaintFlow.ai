import { useState } from 'react'
import { Link } from 'react-router-dom'
import { CameraIcon } from '@heroicons/react/24/solid'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import { snapAndFind, fetchShadeAvailability } from '../../api/customer'

const scanSteps = [
  'Scanning wall surface...',
  'Analyzing pigment composition...',
  'Matching to shade catalog...',
]

export default function SnapAndFind() {
  const [hexInput, setHexInput] = useState('#C41E3A')
  const [result, setResult] = useState(null)
  const [availability, setAvailability] = useState([])
  const [loading, setLoading] = useState(false)
  const [scanStep, setScanStep] = useState(0)
  const [imagePreview, setImagePreview] = useState(null)

  const handleImageUpload = (e) => {
    const file = e.target.files?.[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = () => setImagePreview(reader.result)
    reader.readAsDataURL(file)

    // Extract a color from the center of the image via canvas
    const img = new Image()
    img.onload = () => {
      const canvas = document.createElement('canvas')
      const size = Math.min(img.width, img.height, 800)
      canvas.width = size
      canvas.height = size
      const ctx = canvas.getContext('2d')
      ctx.drawImage(img, 0, 0, size, size)
      const pixel = ctx.getImageData(size / 2, size / 2, 1, 1).data
      const hex = '#' + [pixel[0], pixel[1], pixel[2]].map(c => c.toString(16).padStart(2, '0')).join('')
      setHexInput(hex)
    }
    img.src = URL.createObjectURL(file)
  }

  const handleSearch = async () => {
    setLoading(true)
    setResult(null)
    setAvailability([])

    // Animated scanning steps
    for (let i = 0; i < scanSteps.length; i++) {
      setScanStep(i)
      await new Promise(r => setTimeout(r, 800))
    }

    try {
      const res = await snapAndFind(hexInput)
      setResult(res.data)

      if (res.data.shade_id) {
        const avail = await fetchShadeAvailability(res.data.shade_id, 19.07, 72.87)
        setAvailability(avail.data)
      }
    } catch {
      setResult({ error: 'Failed to find match' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Snap & Find</h1>
        <p className="text-gray-500 mt-1">Upload a photo or pick a color to find the closest shade</p>
      </div>

      {/* Upload area */}
      <div className="border-2 border-dashed border-gray-200 rounded-2xl p-8 text-center hover:border-orange-300 transition-colors relative">
        {imagePreview ? (
          <div className="relative">
            <img src={imagePreview} alt="Uploaded" className="max-h-48 mx-auto rounded-xl" />
            {loading && (
              <div className="absolute inset-0 bg-black/60 rounded-xl flex items-center justify-center">
                <p className="text-white text-sm animate-pulse">{scanSteps[scanStep]}</p>
              </div>
            )}
          </div>
        ) : (
          <>
            <CameraIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p className="text-gray-500 text-sm mb-2">Take a photo of your wall</p>
          </>
        )}
        <input
          type="file"
          accept="image/*"
          capture="environment"
          onChange={handleImageUpload}
          className="absolute inset-0 opacity-0 cursor-pointer"
        />
      </div>

      {/* Or color picker */}
      <div className="flex items-center gap-3">
        <div className="h-px flex-1 bg-gray-200" />
        <span className="text-xs text-gray-400">OR PICK A COLOR</span>
        <div className="h-px flex-1 bg-gray-200" />
      </div>

      <div className="flex gap-3 items-center">
        <input
          type="color"
          value={hexInput}
          onChange={e => setHexInput(e.target.value)}
          className="w-12 h-12 rounded-lg cursor-pointer border-0"
        />
        <input
          type="text"
          value={hexInput}
          onChange={e => setHexInput(e.target.value)}
          className="flex-1 bg-white border border-gray-200 text-gray-900 rounded-lg px-4 py-2 text-sm font-mono outline-none focus:ring-2 focus:ring-orange-300"
          placeholder="#FF0000"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="px-6 py-2.5 bg-orange-500 hover:bg-orange-400 disabled:opacity-50 text-white rounded-lg text-sm font-medium transition-colors"
        >
          {loading ? 'Scanning...' : 'Find Match'}
        </button>
      </div>

      {/* Preview */}
      <div className="flex gap-3">
        <div className="w-20 h-20 rounded-xl border" style={{ backgroundColor: hexInput }} />
        <div className="text-sm text-gray-500 flex flex-col justify-center">
          <p>Selected Color</p>
          <p className="font-mono text-gray-900">{hexInput}</p>
        </div>
      </div>

      {/* Result */}
      {result && !result.error && (
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-lg">
          <h3 className="font-bold text-gray-900 text-lg mb-4">
            Match Found! <span className="text-emerald-600">{result.match?.confidence}% match</span>
          </h3>

          <div className="flex gap-4 mb-4">
            <div className="w-20 h-20 rounded-xl" style={{ backgroundColor: result.detected_color?.hex }} />
            <div className="text-2xl text-gray-300 flex items-center">&rarr;</div>
            <div className="w-20 h-20 rounded-xl" style={{ backgroundColor: result.match?.hex_color }} />
          </div>

          <div className="grid grid-cols-2 gap-3 text-sm mb-4">
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-gray-500">Shade Name</span>
              <p className="font-bold text-gray-900">{result.match?.shade_name}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-gray-500">Code</span>
              <p className="font-mono text-gray-900">{result.match?.shade_code}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-gray-500">Family</span>
              <p className="text-gray-900">{result.match?.shade_family}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <span className="text-gray-500">Product</span>
              <p className="text-gray-900">{result.match?.product_name}</p>
            </div>
          </div>

          <Link
            to={`/customer/shade/${result.shade_id}`}
            className="inline-block px-4 py-2 bg-orange-500 text-white rounded-lg text-sm font-medium hover:bg-orange-400 transition-colors"
          >
            View Details
          </Link>

          {/* Nearby dealers */}
          {availability.length > 0 && (
            <div className="mt-6">
              <h4 className="font-semibold text-gray-900 text-sm mb-2">Available at Nearby Dealers</h4>
              <div className="space-y-2">
                {availability.slice(0, 3).map(d => (
                  <div key={d.dealer_id} className="flex items-center justify-between text-sm bg-gray-50 rounded-lg px-3 py-2">
                    <div>
                      <span className="text-gray-900">{d.dealer_name}</span>
                      <span className="text-gray-400 ml-2">{d.distance_km} km</span>
                    </div>
                    <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                      d.stock_status === 'In Stock' ? 'bg-emerald-100 text-emerald-700' :
                      d.stock_status === 'Low Stock' ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {d.stock_status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {result?.error && (
        <p className="text-red-500 text-center">{result.error}</p>
      )}
    </div>
  )
}
