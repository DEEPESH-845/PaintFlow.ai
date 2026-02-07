import { ArrowRightIcon, TruckIcon } from '@heroicons/react/24/solid'

export default function TransferCard({ props, onConfirm }) {
  const { from, to, sku, qty, eta, savings } = props || {}

  return (
    <div className="bg-gray-800/80 rounded-lg p-4 border border-gray-700 mt-2">
      <div className="flex items-center gap-2 text-xs text-gray-400 mb-3">
        <TruckIcon className="w-4 h-4" />
        <span>Recommended Transfer</span>
      </div>

      <div className="flex items-center justify-between mb-3">
        <div className="text-center">
          <p className="text-sm font-semibold text-white">{from}</p>
          <p className="text-[10px] text-gray-500">Source</p>
        </div>
        <div className="flex items-center gap-2 text-yellow-400">
          <div className="h-px w-8 bg-yellow-400/50" />
          <ArrowRightIcon className="w-4 h-4" />
          <div className="h-px w-8 bg-yellow-400/50" />
        </div>
        <div className="text-center">
          <p className="text-sm font-semibold text-white">{to}</p>
          <p className="text-[10px] text-gray-500">Destination</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 text-xs mb-3">
        <div>
          <span className="text-gray-500">SKU</span>
          <p className="text-white font-medium">{sku}</p>
        </div>
        <div>
          <span className="text-gray-500">Quantity</span>
          <p className="text-white font-medium">{qty} units</p>
        </div>
        <div>
          <span className="text-gray-500">ETA</span>
          <p className="text-white font-medium">{eta}</p>
        </div>
      </div>

      {savings && (
        <p className="text-xs text-emerald-400 mb-3">Potential savings: {savings}</p>
      )}

      <button
        onClick={onConfirm}
        className="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-lg transition-colors"
      >
        Confirm Transfer
      </button>
    </div>
  )
}
