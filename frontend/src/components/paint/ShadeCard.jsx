export default function ShadeCard({ shade }) {
  if (!shade) return null

  return (
    <div className="rounded-xl overflow-hidden bg-white shadow-md">
      <div className="h-40 w-full" style={{ backgroundColor: shade.hex_color }} />
      <div className="p-4">
        <h3 className="text-lg font-bold text-gray-900">{shade.shade_name}</h3>
        <p className="text-sm text-gray-500">{shade.shade_code} | {shade.shade_family}</p>
        <div className="mt-2 flex items-center gap-2 text-xs text-gray-500">
          <span className="inline-block w-4 h-4 rounded border" style={{ backgroundColor: shade.hex_color }} />
          {shade.hex_color}
        </div>
      </div>
    </div>
  )
}
